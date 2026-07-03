from pathlib import Path
import re
import struct


ROOT = Path(__file__).resolve().parents[2]
BANNER = "assets/readme/tradar-readme-banner.png"
EXPECTED = (BANNER, "Tradar README banner", "100%")


def _top_banner(readme: str) -> tuple[str, str, str]:
    block = readme.split("</p>", 1)[0]
    match = re.search(
        r'<img\s+src="([^"]+)"\s+alt="([^"]+)"\s+width="([^"]+)">',
        block,
    )
    assert match is not None
    return match.group(1), match.group(2), match.group(3)


def _png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as fh:
        header = fh.read(24)
    assert header[:8] == b"\x89PNG\r\n\x1a\n"
    return struct.unpack(">II", header[16:24])


def test_readme_variants_use_shared_top_banner() -> None:
    assert _top_banner((ROOT / "README.md").read_text()) == EXPECTED
    assert _top_banner((ROOT / "README.en.md").read_text()) == EXPECTED


def test_readme_banner_asset_matches_expected_ratio() -> None:
    assert _png_size(ROOT / BANNER) == (2172, 724)
