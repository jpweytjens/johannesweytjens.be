# {% snippet panel.py add_pseudodate %} shows one region of a script in
# snippets/, highlighted as {% highlight %} would. A region is marked as in
# vanzelfsprekend (pymdownx.snippets):
#
#     # --8<-- [start:add_pseudodate]
#     ...
#     # --8<-- [end:add_pseudodate]
#
# A missing file or region stops the build, so a renamed marker cannot
# quietly show the wrong code. Markers nested inside the region are dropped,
# and the region is dedented, so a part of a function reads flush left.
module Jekyll
  class SnippetTag < Liquid::Tag
    MARKER = /^\s*# --8<-- \[(start|end):[\w-]+\]\s*$/
    LANGUAGES = { ".py" => "python", ".rb" => "ruby", ".sh" => "bash" }.freeze

    def initialize(tag_name, markup, tokens)
      super
      @file, @name = markup.split
      raise SyntaxError, "usage: {% snippet <file> <region> %}" unless @file && @name
    end

    def render(context)
      site = context.registers[:site]
      path = File.join(site.source, "snippets", @file)
      raise ArgumentError, "snippet: no file snippets/#{@file}" unless File.file?(path)

      lines = File.read(path).gsub("\r\n", "\n").lines
      start = lines.index { |l| l =~ /^\s*# --8<-- \[start:#{Regexp.escape(@name)}\]\s*$/ }
      finish = lines.index { |l| l =~ /^\s*# --8<-- \[end:#{Regexp.escape(@name)}\]\s*$/ }
      unless start && finish && start < finish
        raise ArgumentError, "snippet: no region '#{@name}' in snippets/#{@file}"
      end

      region = lines[(start + 1)...finish].reject { |l| l =~ MARKER }
      indent = region.reject { |l| l.strip.empty? }.map { |l| l[/^ */].size }.min || 0
      code = region.map { |l| l.strip.empty? ? "\n" : l[indent..] }.join.strip

      language = LANGUAGES.fetch(File.extname(@file), "text")
      Liquid::Template.parse(
        "{% highlight #{language} %}{% raw %}\n#{code}\n{% endraw %}{% endhighlight %}"
      ).render!(context)
    end
  end
end

Liquid::Template.register_tag("snippet", Jekyll::SnippetTag)
