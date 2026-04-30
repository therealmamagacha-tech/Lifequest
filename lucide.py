from urllib.parse import quote


def icon_html(name, size=16, color="#00f2ff", css_class="lucide-inline"):
    """Return an HTML <img> tag using Lucide icon from Iconify CDN."""
    encoded_color = quote(color)
    src = f"https://api.iconify.design/lucide:{name}.svg?color={encoded_color}&width={size}&height={size}"
    return (
        f'<img src="{src}" class="{css_class}" '
        f'style="width:{size}px;height:{size}px;vertical-align:middle;" alt="{name}">'
    )
