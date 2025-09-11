CUSTOM_CSS = """
<style>
/* Global Styles */
* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
body, .main, .block-container {
    background: #181a20 !important;
    color: #e5e7eb;
}

/* Main Container */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
    background: #181a20 !important;
}

/* Typography */
.heading {
    text-align: center;
    background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}

.subheading {
    text-align: center;
    font-weight: 500;
    color: #b0b8c1;
    font-size: 1.2rem;
    margin-bottom: 2rem;
    line-height: 1.6;
}

/* Chat Interface */
.chat-container {
    background: #23262f;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 2px 8px 0 rgba(0,0,0,0.25);
    border: 1px solid #23262f;
}

.chat-message {
    background: #23262f;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 2px 0 rgba(0,0,0,0.18);
    border-left: 4px solid #667eea;
    color: #e5e7eb;
}

.user-message {
    border-left-color: #10b981;
    background: linear-gradient(135deg, #1e293b 0%, #23262f 100%);
}

.assistant-message {
    border-left-color: #667eea;
    background: linear-gradient(135deg, #23262f 0%, #181a20 100%);
}

.message-header {
    display: flex;
    align-items: center;
    margin-bottom: 0.75rem;
    font-weight: 600;
    color: #a5b4fc;
}

.user-header {
    color: #34d399;
}

.assistant-header {
    color: #a5b4fc;
}

.message-content {
    line-height: 1.7;
    color: #e5e7eb;
}

/* Chat Input */
.stChatInput, .stTextInput, .stTextArea, textarea, input[type="text"] {
    background: #23262f !important;
    color: #e5e7eb !important;
    border-radius: 12px !important;
    border: 2px solid #353945 !important;
    box-shadow: none !important;
}
.stChatInput:focus-within, .stTextInput:focus-within, .stTextArea:focus-within, textarea:focus, input[type="text"]:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 2px #667eea33 !important;
}

/* Sidebar Styling */
.sidebar .sidebar-content {
    background: #23262f;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 2px 8px 0 rgba(0,0,0,0.18);
}

.sidebar h3 {
    color: #374151;
    font-weight: 700;
    margin-bottom: 1rem;
    font-size: 1.1rem;
}

.sidebar h4 {
    color: #6b7280;
    font-weight: 600;
    margin-bottom: 0.75rem;
    font-size: 1rem;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-weight: 600;
    transition: all 0.2s ease;
    box-shadow: 0 2px 4px rgba(102, 126, 234, 0.2);
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
}

.stButton > button:active {
    transform: translateY(0);
}

/* Selectbox */
.stSelectbox > div > div {
    background: white;
    border: 2px solid #e5e7eb;
    border-radius: 8px;
    transition: border-color 0.2s ease;
}

.stSelectbox > div > div:hover {
    border-color: #667eea;
}

/* Expanders */
.streamlit-expanderHeader {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    border-radius: 8px;
    border: 1px solid #e5e7eb;
    font-weight: 600;
    color: #374151;
}

.streamlit-expanderContent {
    background: white;
    border-radius: 0 0 8px 8px;
    border: 1px solid #e5e7eb;
    border-top: none;
}

/* Metrics */
.metric-container {
    background: #23262f;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 1px 2px 0 rgba(0,0,0,0.18);
    border: 1px solid #353945;
}

.metric-label {
    font-weight: 600;
    color: #b0b8c1;
    font-size: 0.875rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: #e5e7eb;
    margin-top: 0.5rem;
}

/* Tool Calls */
.tool-call {
    background: #181a20;
    border-radius: 8px;
    padding: 1rem;
    margin: 0.5rem 0;
    border-left: 4px solid #f59e0b;
    color: #fbbf24;
}

.tool-name {
    font-weight: 700;
    color: #fbbf24;
    margin-bottom: 0.5rem;
}

.tool-content {
    background: #23262f;
    border-radius: 6px;
    padding: 0.75rem;
    margin-top: 0.5rem;
    border: 1px solid #fbbf24;
    color: #e5e7eb;
}

/* Examples Section */
.examples-container {
    background: #23262f;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    border: 1px solid #353945;
}

.example-button {
    background: linear-gradient(135deg, #434190 0%, #3730a3 100%);
    color: #e5e7eb;
    border: none;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin: 0.25rem;
    font-weight: 600;
    transition: all 0.2s ease;
    box-shadow: 0 1px 2px 0 rgba(0,0,0,0.18);
}

.example-button:hover {
    background: linear-gradient(135deg, #6366f1 0%, #818cf8 100%);
    color: #fff;
    transform: translateY(-1px);
    box-shadow: 0 2px 8px 0 rgba(102, 126, 234, 0.18);
}

/* Status Indicators */
.status-indicator {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 0.5rem;
}

.status-online {
    background: #10b981;
    box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
}

.status-offline {
    background: #ef4444;
    box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.2);
}

/* Loading Animation */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.loading {
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Responsive Design */
@media (max-width: 768px) {
    .heading {
        font-size: 2rem;
    }
    
    .subheading {
        font-size: 1rem;
    }
    
    .chat-container {
        padding: 1rem;
    }
    
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #23262f;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: #353945;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #667eea;
}

/* Links */
a {
    text-decoration: none;
    color: #a5b4fc;
    transition: color 0.2s ease;
    font-weight: 500;
}

a:hover {
    color: #fff;
    text-decoration: underline;
}

/* Code Blocks */
pre {
    background: #23262f;
    color: #e5e7eb;
    border-radius: 8px;
    padding: 1rem;
    overflow-x: auto;
    border: 1px solid #353945;
}

code {
    background: #23262f;
    color: #fbbf24;
    padding: 0.125rem 0.25rem;
    border-radius: 4px;
    font-size: 0.875em;
}

/* Success/Error Messages */
.success-message {
    background: linear-gradient(135deg, #1e293b 0%, #10b98122 100%);
    border: 1px solid #10b98144;
    border-radius: 8px;
    padding: 1rem;
    color: #10b981;
    margin: 1rem 0;
}

.error-message {
    background: linear-gradient(135deg, #23262f 0%, #ef444422 100%);
    border: 1px solid #ef444444;
    border-radius: 8px;
    padding: 1rem;
    color: #ef4444;
    margin: 1rem 0;
}

/* Info Messages */
.info-message {
    background: linear-gradient(135deg, #23262f 0%, #3b82f622 100%);
    border: 1px solid #3b82f644;
    border-radius: 8px;
    padding: 1rem;
    color: #60a5fa;
    margin: 1rem 0;
}
</style>
"""
