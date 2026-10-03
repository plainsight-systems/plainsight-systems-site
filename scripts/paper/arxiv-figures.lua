-- arXiv bundle only (scripts/build-paper.sh --arxiv): arXiv's TeX accepts
-- PDF, PNG and JPG figures but not SVG. The build converts each SVG to a
-- PDF beside it; this points the LaTeX at the converted file.
function Image(img)
  if img.src:match("%.svg$") then
    img.src = img.src:gsub("%.svg$", ".pdf")
    return img
  end
end
