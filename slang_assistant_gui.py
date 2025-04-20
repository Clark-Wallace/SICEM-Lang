import tkinter as tk
from tkinter import ttk, messagebox
from slang_assistant import SlangAssistant
from dotenv import load_dotenv
from gui_styles import (
    ThemeConfig,
    StyledFrame,
    StyledButton,
    StyledLabel,
    StatusLabel,
    ScrollText
)
import os

class SlangAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SICEM-Lang Assistant 🤖")
        self.root.geometry("1200x900")
        
        # Load environment variables
        load_dotenv()
        
        # Set up theme
        ThemeConfig.setup_theme()
        
        # Configure root styling
        self.root.configure(bg=ThemeConfig.COLORS['background'])
        
        # Initialize assistant
        self.assistant = SlangAssistant()
        
        # Create main layout
        self._create_layout()
        
    def _create_layout(self):
        """Create the main layout with styled components."""
        # Header section
        header_frame = StyledFrame(self.root)
        header_frame.pack(fill=tk.X, padx=30, pady=15)
        
        StyledLabel(
            header_frame,
            text="SICEM-Lang Assistant 🤖",
            style_type='Title'
        ).pack(pady=10)
        
        # Status section
        status_frame = StyledFrame(self.root)
        status_frame.pack(fill=tk.X, padx=30, pady=10)
        
        # API Status
        self.api_status = StatusLabel(
            status_frame,
            text="(A)PI Status: Checking... 🔄"
        )
        self.api_status.pack(side=tk.LEFT, padx=10)
        self._check_api_status()
        
        # CI Level
        level_frame = StyledFrame(status_frame)
        level_frame.pack(side=tk.RIGHT, padx=10)
        
        StyledLabel(
            level_frame,
            text="(L)evel of understanding? 🧠",
            style_type='Subtitle'
        ).pack(side=tk.LEFT, padx=10)
        
        self.ci_level = tk.DoubleVar(value=0.7)  # Default to higher CI level
        ttk.Scale(
            level_frame,
            from_=0.0,
            to=1.0,
            variable=self.ci_level,
            orient=tk.HORIZONTAL,
            length=250,
            command=self._update_ci_level
        ).pack(side=tk.LEFT, padx=10)
        
        # Main content area
        content_frame = StyledFrame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)
        
        # Conversation area
        conversation_frame = StyledFrame(content_frame)
        conversation_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        StyledLabel(
            conversation_frame,
            text="Conversation 💭",
            style_type='Subtitle'
        ).pack(anchor=tk.W, pady=10)
        
        self.conversation_area = ScrollText(
            conversation_frame,
            width=80,
            height=25,
            bg=ThemeConfig.COLORS['card_bg'],
            fg=ThemeConfig.COLORS['text_primary'],
            relief=tk.SOLID,
            borderwidth=1,
            padx=10,
            pady=5
        )
        self.conversation_area.pack(fill=tk.BOTH, expand=True)
        self.conversation_area.config(state=tk.DISABLED)
        
        # Input area
        input_frame = StyledFrame(content_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        StyledLabel(
            input_frame,
            text="(T)ype your command 💭",
            style_type='Subtitle'
        ).pack(anchor=tk.W, pady=10)
        
        # Create a frame specifically for the input box
        input_box_frame = tk.Frame(input_frame, bg=ThemeConfig.COLORS['card_bg'])
        input_box_frame.pack(fill=tk.X, padx=5)
        
        self.input_area = tk.Text(
            input_box_frame,
            width=80,
            height=4,
            wrap=tk.WORD,
            font=ThemeConfig.FONTS['body'],
            bg=ThemeConfig.COLORS['card_bg'],
            fg=ThemeConfig.COLORS['text_primary'],
            relief=tk.SOLID,
            borderwidth=1,
            padx=10,
            pady=5,
            insertbackground=ThemeConfig.COLORS['text_primary']  # Make cursor visible
        )
        self.input_area.pack(fill=tk.X, expand=True)
        
        # Button bar
        button_frame = StyledFrame(content_frame)
        button_frame.pack(fill=tk.X, pady=15)
        
        StyledButton(
            button_frame,
            text="(S)end ✉️",
            command=self._send_message
        ).pack(side=tk.LEFT, padx=10)
        
        StyledButton(
            button_frame,
            text="(F)ile 💾",
            command=self._save_draft,
            style_type='Secondary'
        ).pack(side=tk.LEFT, padx=10)
        
        StyledButton(
            button_frame,
            text="(N)ew 🆕",
            command=self._new_draft,
            style_type='Secondary'
        ).pack(side=tk.LEFT, padx=10)
        
        StyledButton(
            button_frame,
            text="(H)elp ❓",
            command=self._show_help,
            style_type='Secondary'
        ).pack(side=tk.LEFT, padx=10)
        
        # Add welcome message
        self._add_to_conversation("Assistant", "(H)ey! Let's create something epic! 🚀\n" + \
                                "(S)imple function - tell me what it should do\n" + \
                                "(B)asic task - describe it in your words\n" + \
                                "(E)asy feature - what's the main idea?")
        
    def _check_api_status(self):
        """Check and update API status."""
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.api_status.set_status(
                'success',
                "(A)PI Status: Connected! 🟢"
            )
        else:
            self.api_status.set_status(
                'error',
                "(A)PI Status: Not Connected! 🔴"
            )
            
    def _update_ci_level(self, *args):
        """Update CI level with EIRS feedback."""
        self.assistant = SlangAssistant(user_ci_level=self.ci_level.get())
        self._add_to_conversation(
            "System",
            f"(L)evel set to {self.ci_level.get():.1f} 🎯"
        )
        
    def _send_message(self):
        """Process and send message with EIRS style."""
        user_input = self.input_area.get("1.0", tk.END).strip()
        if not user_input:
            return
            
        # Add user message to conversation
        self._add_to_conversation("You", user_input)
        
        # Clear input area
        self.input_area.delete("1.0", tk.END)
        
        try:
            # Get assistant response
            response = self.assistant.process_user_input(user_input)
            
            # Add assistant response to conversation
            self._add_to_conversation("Assistant", response)
            
        except Exception as e:
            self._add_to_conversation(
                "System",
                f"(E)rror processing message: {str(e)} 😅"
            )
        
    def _add_to_conversation(self, speaker: str, message: str):
        """Add message to conversation with EIRS style."""
        self.conversation_area.config(state=tk.NORMAL)
        
        # Configure tag for speaker
        tag = f"speaker_{speaker.lower()}"
        if not tag in self.conversation_area.tag_names():
            if speaker == "Assistant":
                self.conversation_area.tag_configure(tag, foreground=ThemeConfig.COLORS['primary'], font=(ThemeConfig.FONTS['body'][0], ThemeConfig.FONTS['body'][1], 'bold'))
            elif speaker == "System":
                self.conversation_area.tag_configure(tag, foreground=ThemeConfig.COLORS['secondary'], font=(ThemeConfig.FONTS['body'][0], ThemeConfig.FONTS['body'][1], 'bold'))
            else:
                self.conversation_area.tag_configure(tag, foreground=ThemeConfig.COLORS['text_primary'], font=(ThemeConfig.FONTS['body'][0], ThemeConfig.FONTS['body'][1], 'bold'))
        
        # Insert speaker with tag
        start_idx = self.conversation_area.index("end-1c")
        self.conversation_area.insert(tk.END, f"{speaker}: ")
        end_idx = self.conversation_area.index("end-1c")
        self.conversation_area.tag_add(tag, start_idx, end_idx)
        
        # Insert message
        self.conversation_area.insert(tk.END, f"{message}\n\n")
        self.conversation_area.see(tk.END)
        self.conversation_area.config(state=tk.DISABLED)
        
    def _save_draft(self):
        """Save draft with EIRS feedback."""
        try:
            draft = self.assistant.get_current_draft()
            if not draft["system"]:
                messagebox.showwarning(
                    "Hold up! ⚠️",
                    "(N)o system yet!\n" + \
                    "(C)reate a system first"
                )
                return
                
            filename = f"{draft['system']}.slang"
            result = self.assistant.save_draft(filename)
            self._add_to_conversation("System", result)
            
        except Exception as e:
            self._add_to_conversation(
                "System",
                f"(E)rror saving draft: {str(e)} 😅"
            )
        
    def _new_draft(self):
        """Start new draft with EIRS style."""
        try:
            self.assistant.reset_draft()
            self._add_to_conversation(
                "System",
                "(N)ew system started! 🎨\n" + \
                "(S)imple function - tell me what it should do\n" + \
                "(B)asic task - describe it in your words\n" + \
                "(E)asy feature - what's the main idea?"
            )
        except Exception as e:
            self._add_to_conversation(
                "System",
                f"(E)rror resetting draft: {str(e)} 😅"
            )
        
    def _show_help(self):
        """Show help with EIRS style."""
        help_text = """
        Quick Guide:
        
        (A)PI Status - Shows if OpenAI is connected
        (L)evel slider - Set your understanding level 🎚️
        (T)ype commands - Use first letters for quick actions 💬
        (S)end - Process your command ✉️
        (F)ile - Save your system 💾
        (N)ew - Start fresh 🆕
        (H)elp - Show this guide ❓
        
        Understanding Levels:
        - 0.0-0.3: (S)imple mode 😊
        - 0.3-0.6: (M)edium mode 🎵
        - 0.6-1.0: (A)dvanced mode 🚀
        """
        messagebox.showinfo("Need Help? 🤔", help_text)

def main():
    root = tk.Tk()
    app = SlangAssistantGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 