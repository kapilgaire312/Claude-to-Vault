def get_user_prompt_for_file_paths(vault_files_info, messages):
    return f"""
Analyze the following new chat messages and determine the routing strategy.

---
CURRENT VAULT INDEX:
    {vault_files_info}
*(If this is empty, there are no existing notes).*

---
NEW CHAT MESSAGES (The Delta):
{messages}

---
TASK:
1. Identify the core technical concepts discussed in depth in the New Chat Messages.
2. Compare them against the Current Vault Index.
3. Output the JSON routing map specifying which existing files to update, and which new files to create.
    """
