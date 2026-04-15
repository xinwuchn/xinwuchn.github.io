require 'net/http'
require 'json'
require 'yaml'
require 'uri'
require 'time'
require 'fileutils'

# Fetches citation counts from Semantic Scholar at build time and exposes
# them to Liquid templates as `site.data.citations.counts[<doi>]`.
#
# Results are cached in `_data/citations.yml` and refreshed at most once per
# CACHE_TTL seconds (default: 24 h). Network failures are non-fatal — the
# previous cache is kept and a warning is logged.
module SemanticScholarCitations
  CACHE_FILE = File.join('_data', 'citations.yml')
  CACHE_TTL  = 24 * 3600
  BATCH_URL  = 'https://api.semanticscholar.org/graph/v1/paper/batch?fields=citationCount'

  def self.load_cache(source)
    path = File.join(source, CACHE_FILE)
    return {} unless File.exist?(path)
    YAML.load_file(path) || {}
  rescue
    {}
  end

  def self.save_cache(source, data)
    path = File.join(source, CACHE_FILE)
    FileUtils.mkdir_p(File.dirname(path))
    File.write(path, data.to_yaml)
  end

  def self.extract_dois(bib_path)
    return [] unless File.exist?(bib_path)
    content = File.read(bib_path)
    content.scan(/doi\s*=\s*[{"]([^{}"]+)["}]/i)
           .flatten
           .map { |d| d.strip.downcase }
           .reject(&:empty?)
           .uniq
  end

  def self.fetch_counts(dois)
    return {} if dois.empty?
    uri = URI(BATCH_URL)
    req = Net::HTTP::Post.new(uri, 'Content-Type' => 'application/json')
    req.body = { ids: dois.map { |d| "DOI:#{d}" } }.to_json
    res = Net::HTTP.start(uri.host, uri.port, use_ssl: true, open_timeout: 10, read_timeout: 30) do |http|
      http.request(req)
    end
    unless res.is_a?(Net::HTTPSuccess)
      Jekyll.logger.warn 'SemanticScholar:', "HTTP #{res.code}: #{res.body[0, 200]}"
      return {}
    end
    results = JSON.parse(res.body)
    map = {}
    dois.each_with_index do |doi, i|
      entry = results[i]
      map[doi] = entry['citationCount'] if entry.is_a?(Hash) && entry['citationCount']
    end
    map
  rescue => e
    Jekyll.logger.warn 'SemanticScholar:', "fetch failed: #{e.message}"
    {}
  end
end

Jekyll::Hooks.register :site, :post_read do |site|
  next if ENV['JEKYLL_DISABLE_SEMANTIC_SCHOLAR']

  cache = SemanticScholarCitations.load_cache(site.source)
  counts = cache['counts'] || {}
  updated_at = cache['updated_at']

  stale =
    updated_at.nil? ||
    (Time.now - Time.parse(updated_at.to_s)) > SemanticScholarCitations::CACHE_TTL

  if stale
    bib_path = File.join(site.source, '_bibliography', 'papers.bib')
    dois = SemanticScholarCitations.extract_dois(bib_path)
    if dois.any?
      Jekyll.logger.info 'SemanticScholar:', "fetching citation counts for #{dois.size} DOIs"
      fresh = SemanticScholarCitations.fetch_counts(dois)
      if fresh.any?
        counts = counts.merge(fresh)
        SemanticScholarCitations.save_cache(site.source, {
          'updated_at' => Time.now.utc.iso8601,
          'counts' => counts
        })
        Jekyll.logger.info 'SemanticScholar:', "updated #{fresh.size} entries"
      end
    end
  end

  site.data['citations'] = { 'counts' => counts }
end
