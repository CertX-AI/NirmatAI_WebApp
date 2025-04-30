"""Locking mechanism module of NirmatAI WebApp."""
import logging
import os
import shutil
import time
import uuid

import streamlit as st

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define lock file and constants
LOCK_FILE = "nirmatai_webapp.lock"
MAX_LOCK_DURATION = 1800  # 30 minutes


def acquire_lock() -> bool:
    """Attempt to acquire the lock atomically and store a unique token.

    Returns:
    bool: True if lock acquired successfully, False if lock file already exists.
    """
    try:
        # Generate a unique token
        lock_token = str(uuid.uuid4())

        # Check if username exists in session state
        if "username" not in st.session_state:
            raise ValueError("Session state 'username' is not initialized.")

        # Atomically create the lock file
        fd = os.open(LOCK_FILE, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        with os.fdopen(fd, "w") as f:
            f.write(f"{st.session_state['username']}\n")
            f.write(f"{lock_token}\n")
            f.write(str(time.time()) + "\n")
            f.write(str(MAX_LOCK_DURATION))

        # Store the lock token in session state
        st.session_state["lock_token"] = lock_token
        logging.info("Lock acquired successfully.")
        return True
    except FileExistsError:
        logging.warning("Lock file already exists.")
        return False
    except Exception as e:
        logging.error(f"Error acquiring lock: {e}")
        return False


def is_locked() -> bool:
    """Check if the lock file exists and is valid.

    Returns:
    bool: True if lock file exists and is valid, False if lock is stale or not present.
    """
    try:
        if os.path.exists(LOCK_FILE):
            with open(LOCK_FILE) as f:
                lines = f.readlines()
                if len(lines) >= 4:
                    lock_time = float(lines[2].strip())
                    lock_duration = float(lines[3].strip())  # Read lock duration
                    if time.time() - lock_time > lock_duration:
                        # Lock is stale; remove it
                        os.remove(LOCK_FILE)
                        logging.info("Stale lock file removed.")
                        return False
                    return True
        return False
    except Exception as e:
        logging.error(f"Error checking lock status: {e}")
        return False


def release_lock(time_flag: bool = False) -> None:
    """Attempt to release the lock only if the token matches.

    Parameters:
    time_flag (bool): If True, the lock will be released even if tokens do not match.
    """
    try:
        if os.path.exists(LOCK_FILE):
            with open(LOCK_FILE) as f:
                lines = f.readlines()
                if len(lines) >= 3:
                    lock_username = lines[0].strip()
                    lock_token = lines[1].strip()

                    # Check if session state has 'username' and 'lock_token'
                    if "username" not in st.session_state or "lock_token" not in st.session_state: # noqa: E501
                        raise ValueError(
                            "Session 'username' or 'lock_token' is not initialized."
                        )

                    # Compare tokens
                    if lock_username == st.session_state["username"] and lock_token == st.session_state.get("lock_token", ""): # noqa: E501
                        os.remove(LOCK_FILE)
                        del st.session_state["lock_token"]
                        logging.info("Lock released successfully.")
                    elif time_flag:
                        # Token expired; release the lock
                        os.remove(LOCK_FILE)
                        del st.session_state["lock_token"]
                        logging.info("Lock released due to expiration.")
                    else:
                        st.error("You do not have permission to release this lock.")
                        logging.warning(
                            "Attempted to release lock without matching token."
                        )
                else:
                    # Lock file is corrupted or invalid
                    os.remove(LOCK_FILE)
                    logging.warning("Corrupted lock file removed.")
        else:
            st.warning("Lock file does not exist.")
            logging.info("Lock file does not exist when attempting to release.")
    except Exception as e:
        logging.error(f"Error releasing lock: {e}")


def update_lock_duration(new_duration: int) -> bool:
    """Update the maximum lock duration and modify the lock file if it exists.

    Parameters:
    new_duration (int): The new maximum lock duration in seconds.

    Returns:
    bool: True if the lock duration was updated successfully, False otherwise.
    """
    global MAX_LOCK_DURATION
    if new_duration > MAX_LOCK_DURATION:
        MAX_LOCK_DURATION = new_duration

        try:
            if os.path.exists(LOCK_FILE):
                with open(LOCK_FILE) as f:
                    lines = f.readlines()

                if len(lines) >= 4:
                    lines[3] = str(new_duration) + "\n"

                    with open(LOCK_FILE, "w") as f:
                        f.writelines(lines)
                    logging.info("Lock file duration updated successfully.")
                    return True

            logging.info(
                "Lock duration updated in memory. No active lock file to modify."
            )
            return True
        except Exception as e:
            logging.error(f"Error updating lock duration: {e}")
            return False
    else:
        logging.info(
            "Calculated duration is not greater than the current MAX_LOCK_DURATION."
        )
        return False


def get_remaining_lock_time() -> float | None:
    """Calculate the remaining time of the lock.

    Returns:
    float | None: The remaining time before lock expires, or None if no lock exists.
    """
    try:
        if os.path.exists(LOCK_FILE):
            with open(LOCK_FILE) as f:
                lines = f.readlines()
                if len(lines) >= 4:
                    lock_time = float(lines[2].strip())
                    lock_duration = float(lines[3].strip())
                    remaining_time = (lock_time + lock_duration) - time.time()
                    return max(0, remaining_time)
        return None
    except Exception as e:
        logging.error(f"Error calculating remaining lock time: {e}")
        return None


def get_lock_info() -> tuple[str | None, float | None]:
    """Get the username and timestamp from the lock file.

    Returns:
    tuple[str | None, float | None]: A tuple containing
                lock owner's username and timestamp,
                or (None, None) if the lock file does not exist or is invalid.
    """
    try:
        if os.path.exists(LOCK_FILE):
            with open(LOCK_FILE) as f:
                lines = f.readlines()
                if len(lines) >= 4:
                    lock_username = lines[0].strip()
                    lock_time = float(lines[2].strip())
                    return lock_username, lock_time
        return None, None
    except Exception as e:
        logging.error(f"Error retrieving lock info: {e}")
        return None, None


def remove_user_folder(username: str) -> None:
    """Removes the folder for a specific user and all its contents.

    Parameters:
    username (str): The username whose folder will be removed.
    """
    try:
        if not username:
            raise ValueError("Username must not be empty.")

        user_folder = os.path.join("uploaded_files", username)

        if os.path.exists(user_folder):
            shutil.rmtree(user_folder)
            logging.info(f"User folder '{username}' removed successfully.")
        else:
            logging.warning(f"User folder '{username}' does not exist.")
    except Exception as e:
        logging.error(f"Error removing user folder '{username}': {e}")
