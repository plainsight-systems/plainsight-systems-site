-- Papers use ## for top-level sections because the web page title is the
-- h1. Shift every heading up one level before pandoc-crossref and LaTeX
-- see it, so sections number 1, 2, ... (pandoc's --shift-heading-level-by
-- runs after filters, too late for crossref). web-body.lua shifts the web
-- output back. A single-# heading in a paper is an error.
function Header(h)
  if h.level == 1 then
    error("papers use ## for top-level sections; found '# " .. pandoc.utils.stringify(h) .. "'")
  end
  h.level = h.level - 1
  return h
end
