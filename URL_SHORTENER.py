import string
import random
from abc import ABC, abstractmethod


# ---------------------------
# Strategy Pattern for Code Generation
# ---------------------------

class CodeGenerator(ABC):
    @abstractmethod
    def generate(self, long_url: str) -> str:
        pass


class RandomCodeGenerator(CodeGenerator):
    def __init__(self, length: int = 6):
        self.length = length
        self.chars = string.ascii_letters + string.digits

    def generate(self, long_url: str) -> str:
        return ''.join(random.choice(self.chars) for _ in range(self.length))


class Base62CodeGenerator(CodeGenerator):
    """Encodes incremental IDs into Base62 for predictable short codes"""
    def __init__(self):
        self.counter = 1000
        self.chars = string.ascii_letters + string.digits

    def generate(self, long_url: str) -> str:
        num = self.counter
        self.counter += 1
        base62 = []
        while num > 0:
            num, rem = divmod(num, 62)
            base62.append(self.chars[rem])
        return ''.join(reversed(base62))


# ---------------------------
# URL Shortener Service
# ---------------------------

class URLShortener:
    def __init__(self, domain: str, generator: CodeGenerator):
        self.domain = domain
        self.generator = generator
        self.long_to_short = {}
        self.short_to_long = {}

    def shorten(self, long_url: str, custom_alias: str = None) -> str:
        # Already shortened
        if long_url in self.long_to_short:
            return self.domain + "/" + self.long_to_short[long_url]

        # Custom alias
        if custom_alias:
            if custom_alias in self.short_to_long:
                raise Exception("Alias already taken!")
            code = custom_alias
        else:
            # Generate unique code
            code = self.generator.generate(long_url)
            while code in self.short_to_long:
                code = self.generator.generate(long_url)

        # Save mappings
        self.long_to_short[long_url] = code
        self.short_to_long[code] = long_url

        return self.domain + "/" + code

    def expand(self, short_url: str) -> str:
        code = short_url.split("/")[-1]
        if code not in self.short_to_long:
            raise Exception("Short URL not found!")
        return self.short_to_long[code]


# ---------------------------
# Demo
# ---------------------------

if __name__ == "__main__":
    # Using random strategy
    shortener1 = URLShortener("http://short.ly", RandomCodeGenerator())

    long1 = "https://www.example.com/some/very/long/path"
    s1 = shortener1.shorten(long1)
    print("Shortened:", s1)
    print("Expanded:", shortener1.expand(s1))

    # Using Base62 strategy
    shortener2 = URLShortener("http://tiny.cc", Base62CodeGenerator())

    long2 = "https://openai.com/research/gpt"
    s2 = shortener2.shorten(long2)
    print("\nShortened:", s2)
    print("Expanded:", shortener2.expand(s2))

    # Custom alias
    s3 = shortener2.shorten("https://github.com/openai", custom_alias="openaihub")
    print("\nShortened with alias:", s3)
    print("Expanded:", shortener2.expand(s3))
