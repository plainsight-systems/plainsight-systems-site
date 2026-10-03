-- Maps the site's paper front matter onto pandoc's LaTeX template
-- variables, for the PDF only (scripts/build-paper.sh).
--
--   authors: [{given, family}]   -> author: ["Given Family", ...]
--   status, version, date        -> date: "Working paper · Version 0.1 · 3 October 2026"
--   paper-url (set by the build)  -> appended to the date line, so a shared
--                                    PDF links back to its web page
--   authors + date                -> copyright line: "© 2026 Given Family,
--                                    CC BY 4.0" (papers are copyright their authors)
--   unlabelled code blocks        -> wrapping Verbatim (see pdf-header.tex)
--
-- Errors on a malformed date or unknown status rather than printing a
-- wrong title block. The web page validates the same fields in
-- layouts/partials/paper/validate.html.

local stringify = pandoc.utils.stringify

local MONTHS = {
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December",
}

local STATUS = {
  ["working-paper"] = "Working paper",
  ["preprint"] = "Preprint",
  ["published"] = "Published",
}

function Meta(m)
  if not m.authors or #m.authors == 0 then
    error("paper front matter: at least one author is required")
  end
  local names = pandoc.List()
  for _, a in ipairs(m.authors) do
    if not a.given or not a.family then
      error("paper front matter: every author needs given and family names")
    end
    names:insert(pandoc.MetaString(stringify(a.given) .. " " .. stringify(a.family)))
  end
  m.author = names

  local date = stringify(m.date or "")
  local y, mo, d = date:match("^(%d%d%d%d)%-(%d%d)%-(%d%d)$")
  if not y then
    error("paper front matter: date must be YYYY-MM-DD, got '" .. date .. "'")
  end

  local status = STATUS[stringify(m.status or "")]
  if not status then
    error("paper front matter: status must be working-paper, preprint or published")
  end
  if not m.version then
    error("paper front matter: version is required")
  end

  local line = string.format("%s · Version %s · %d %s %s",
    status, stringify(m.version), tonumber(d), MONTHS[tonumber(mo)], y)
  local inlines = pandoc.List{pandoc.Str(line)}
  if m["paper-url"] then
    local url = stringify(m["paper-url"])
    inlines:insert(pandoc.LineBreak())
    inlines:insert(pandoc.Link(url, url))
  end
  local holders = {}
  for _, n in ipairs(names) do holders[#holders + 1] = stringify(n) end
  local joined = #holders > 1
    and table.concat(holders, ", ", 1, #holders - 1) .. " and " .. holders[#holders]
    or holders[1]
  inlines:insert(pandoc.LineBreak())
  inlines:insert(pandoc.Str("© " .. y .. " " .. joined .. " · "))
  inlines:insert(pandoc.Link("CC BY 4.0", "https://creativecommons.org/licenses/by/4.0/"))
  m.date = pandoc.MetaInlines(inlines)
  return m
end

-- Code blocks without a language are not highlighted, so pandoc would emit
-- plain verbatim, which cannot wrap. Emit fvextra's Verbatim instead.
function CodeBlock(cb)
  if #cb.classes == 0 then
    return pandoc.RawBlock("latex",
      "\\begin{Verbatim}[breaklines,breakanywhere]\n" .. cb.text .. "\n\\end{Verbatim}")
  end
end
