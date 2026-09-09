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


def get_user_prompt_for_new_note(
    vault_files_to_be_modified, current_file_path, chat_messages
):
    return f"""
--- THE MASTER PLAN (Vault Map for Cross-Linking) ---
    {vault_files_to_be_modified}

--- ASSIGNED FILE SCOPE ---
Target File Path: {current_file_path}

--- CONVERSATION TRANSCRIPT (The Delta) ---
            {chat_messages}

--- INSTRUCTIONS ---
Synthesize the conversation above into a permanent technical reference for '{current_file_path}'.
Make sure to reflect the Developer's inquiries, compare the alternative options discussed, and follow the exact required Markdown schema.
    """


def get_user_prompt_for_note_update(
    vault_files_to_be_modified, current_file_path, chat_messages
):
    return f"""
--- THE MASTER PLAN (Vault Map for Cross-Linking) ---
    {vault_files_to_be_modified}

--- ASSIGNED FILE SCOPE ---
Target File Path: {current_file_path}

--- EXISTING NOTE CONTENT ---
   {chat_messages}

--- INSTRUCTIONS ---
Surgically integrate the New Knowledge into the Existing Note Content for '{current_file_path}'.
- Weave new explanations, code, and trade-offs into their respective sections.
- Preserve all user inline annotations (==...== and <!--...-->).
- Add new recall questions to the bottom of the list.
- Return the complete, updated Markdown document.
  """
