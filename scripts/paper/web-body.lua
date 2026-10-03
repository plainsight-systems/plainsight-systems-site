-- Reshapes pandoc-crossref output into markdown that Hugo's Goldmark and
-- the site's render hooks understand. Web output only; runs after
-- pandoc-crossref (scripts/build-paper.sh).
--
--   Figure #fig:x  -> <div id="fig:x"> around a standalone image. The
--                     image hook (layouts/_markup/render-image.html)
--                     numbers figures in document order, the same order
--                     pandoc-crossref and LaTeX use; crossref is run with
--                     figureTemplate "$$t$$" so the caption is not
--                     numbered twice.
--   Table #tbl:x   -> <div id="tbl:x"> holding a caption paragraph
--                     ("Table 1. ...") above the table. Goldmark has no
--                     table captions.
--   Equation #eq:x -> <div id="eq:x"> around the display math, numbered
--                     by KaTeX's \tag (crossref equationNumberTeX).
--   Headings       -> shifted back down one level. The build shifts ## to
--                     level 1 so crossref numbers sections 1, 2, ...;
--                     Hugo needs them as h2 under the page title.
--
-- Every figure must carry a #fig: label: LaTeX numbers all figures, and
-- crossref numbers only labelled ones, so an unlabelled figure would make
-- the web and PDF numbering disagree.

local function caption_inlines(caption)
  local out = pandoc.List()
  for _, block in ipairs(caption.long or {}) do
    if #out > 0 then out:insert(pandoc.Space()) end
    out:extend(block.content or {})
  end
  return out
end

function Figure(fig)
  local id = fig.identifier or ""
  if not id:match("^fig:") then
    error("every figure needs a {#fig:label}; found one with id '" .. id .. "'")
  end
  local image
  fig.content:walk({ Image = function(img) image = image or img end })
  if not image then
    error("figure " .. id .. " has no image")
  end
  local img = pandoc.Image(caption_inlines(fig.caption), image.src, "")
  return pandoc.Div({ pandoc.Para({ img }) }, pandoc.Attr(id))
end

function Table(tbl)
  local id = tbl.identifier or ""
  local cap = caption_inlines(tbl.caption)
  if id == "" and #cap == 0 then return nil end
  tbl.caption = pandoc.Caption()
  tbl.identifier = ""
  local blocks = pandoc.List()
  if #cap > 0 then
    blocks:insert(pandoc.Div({ pandoc.Para(cap) }, pandoc.Attr("", { "ps-table-caption" })))
  end
  blocks:insert(tbl)
  return pandoc.Div(blocks, pandoc.Attr(id, { "ps-table" }))
end

-- crossref wraps a labelled equation in a Span inside its paragraph.
function Para(para)
  if #para.content == 1 and para.content[1].t == "Span"
     and para.content[1].identifier:match("^eq:") then
    local span = para.content[1]
    return pandoc.Div({ pandoc.Para(span.content) }, pandoc.Attr(span.identifier, { "ps-equation" }))
  end
end

function Header(h)
  h.level = h.level + 1
  return h
end
