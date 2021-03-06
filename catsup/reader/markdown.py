import misaka as m
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound
from tornado.escape import xhtml_escape


class CatsupRender(m.HtmlRenderer, m.SmartyPants):
    def block_code(self, text, lang):
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except ClassNotFound:
            text = xhtml_escape(text.strip())
            return '\n<pre><code>%s</code></pre>\n' % text
        else:
            formatter = HtmlFormatter()
            return highlight(text, lexer, formatter)

    def autolink(self, link, is_email):
        if is_email:
            s = '<a href="mailto:{link}">{link}</a>'
        elif link.endswith(('.jpg', '.png', '.git', '.jpeg')):
            s = '<a href="{link}"><img src="{link}" /></a>'
        else:
            s = '<a href="{link}">{link}</a>'
        return s.format(link=link)

# Allow use raw html in .md files
md_raw = m.Markdown(CatsupRender(flags=m.HTML_USE_XHTML),
    extensions=m.EXT_FENCED_CODE |
               m.EXT_NO_INTRA_EMPHASIS |
               m.EXT_AUTOLINK |
               m.EXT_STRIKETHROUGH |
               m.EXT_SUPERSCRIPT)

md_escape = m.Markdown(CatsupRender(flags=m.HTML_ESCAPE | m.HTML_USE_XHTML),
    extensions=m.EXT_FENCED_CODE |
               m.EXT_NO_INTRA_EMPHASIS |
               m.EXT_AUTOLINK |
               m.EXT_STRIKETHROUGH |
               m.EXT_SUPERSCRIPT)
