import os
import json
import logging

logger = logging.getLogger(__name__)

def get_version() -> str:
    """
    Fetches the service version from the .release-please-manifest.json
    file in the project's root directory.

    Returns:
        A string containing the version, e.g., "1.2.3", or a
        default/error string if the file cannot be read.
    """
    manifest_path = os.path.join(os.getcwd(), '.release-please-manifest.json')
    
    try:
        with open(manifest_path, 'r') as f:
            data = json.load(f)
            # The version number is stored under the "." key
            return data.get('.', '0.0.0-unknown')
    except FileNotFoundError:
        logger.warning(f"Version manifest not found at: {manifest_path}. Defaulting to dev version.")
        return "0.0.0-dev"
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Error parsing version manifest {manifest_path}: {e}")
        return "0.0.0-invalid"
