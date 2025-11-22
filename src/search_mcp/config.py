import tomllib
import shutil
from pathlib import Path
from typing import Any

class Config:
    _instance = None
    _config_data: dict[str, Any] = {}
    _config_path: Path = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _get_config_path(self) -> Path:
        user_config_dir = Path.home() / ".config" / "search-mcp"
        user_config_file = user_config_dir / "config.toml"
        
        if user_config_file.exists():
            return user_config_file
        
        dev_config_file = Path(__file__).parent.parent.parent / "config.toml"
        if dev_config_file.exists():
            return dev_config_file
        
        return user_config_file
    
    def _create_default_config(self, config_path: Path):
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        example_file = Path(__file__).parent.parent.parent / "config.toml.example"
        if example_file.exists():
            shutil.copy(example_file, config_path)
        else:
            default_content = """[debug]
enabled = false

[grok]
api_url = "https://cc.guda.studio/grok/v1"
api_key = "YOUR_API_KEY_HERE"

[logging]
level = "INFO"
dir = "logs"
"""
            config_path.write_text(default_content, encoding="utf-8")
    
    def _load_config(self):
        self._config_path = self._get_config_path()
        
        if not self._config_path.exists():
            self._create_default_config(self._config_path)
            raise FileNotFoundError(
                f"Configuration file created at: {self._config_path}\n"
                f"Please edit it with your API credentials and restart."
            )
        
        with open(self._config_path, "rb") as f:
            self._config_data = tomllib.load(f)
    
    @property
    def debug_enabled(self) -> bool:
        return self._config_data.get("debug", {}).get("enabled", False)
    
    @property
    def grok_api_url(self) -> str:
        url = self._config_data.get("grok", {}).get("api_url")
        if not url:
            raise ValueError("grok.api_url not configured")
        return url
    
    @property
    def grok_api_key(self) -> str:
        key = self._config_data.get("grok", {}).get("api_key")
        if not key:
            raise ValueError("grok.api_key not configured")
        return key
    
    @property
    def log_level(self) -> str:
        return self._config_data.get("logging", {}).get("level", "INFO")
    
    @property
    def log_dir(self) -> Path:
        log_dir_str = self._config_data.get("logging", {}).get("dir", "logs")
        if Path(log_dir_str).is_absolute():
            return Path(log_dir_str)
        user_log_dir = Path.home() / ".config" / "search-mcp" / log_dir_str
        return user_log_dir
    
    @property
    def config_path(self) -> Path:
        return self._config_path

config = Config()
