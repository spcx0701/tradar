from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VIDEO_ID = "bNExkDu3g-o"


def test_readme_links_to_service_video_with_thumbnail():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert f"https://youtu.be/{VIDEO_ID}" in readme
    assert f"https://i.ytimg.com/vi/{VIDEO_ID}/hqdefault.jpg" in readme
    assert "Tradar 소개 영상" in readme


def test_landing_embeds_service_video_section():
    landing = (ROOT / "app" / "index.html").read_text(encoding="utf-8")

    assert 'id="service-video"' in landing
    assert f"https://www.youtube.com/embed/{VIDEO_ID}" in landing
    assert "서비스 영상" in landing
