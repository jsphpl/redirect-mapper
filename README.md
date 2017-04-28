# redirect-mapper

Takes two lists of URLs and outputs a mapping that assigns each entry in list 1 an item from list 2 along with a score that indicates how likely the two refer to the same thing.

## Use case

This script was created to automatically generate a map of redirects when migrating a website. The input lists would be a sitemap of each the old and new website, both plain text files containing one url per line. The URLs are required to be "pretty", meaning not just `/post.php?id=123` but rather something like `/blog/why-wordpress-sucks` and ideally have their protocol- and domain parts removed.

It can of course be used as a generic tool to fuzzy match two sets of strings. It uses the [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) metric as implemented by [python-Levenshtein](https://rawgit.com/ztane/python-Levenshtein/master/docs/Levenshtein.html#Levenshtein-ratio).

## Usage

1. Clone this repository `git clone https://github.com/jsphpl/redirect-mapper`
2. Enter it `cd redirect-mapper`
3. Install dependencies `python setup.py`
4. Use it:

```
$ python map.py [-h] [-a] [-t T] [-c PATH] list1 list2

Generates a redirect map from two sitemaps for website migration. By default,
all matches are dumped on the standard output. If an item from list1 is
exactly contained in list2, it will be assigned directly, without calculating
distance or checking for ambiguity.

positional arguments:
  list1                 List of target items for which to find matches. (1
                        item per line)
  list2                 List of search items on which to search for matches.
                        (1 item per line)

optional arguments:
  -h, --help            show this help message and exit
  -t VALUE, --threshold VALUE
                        Range within which two scores are considered equal.
                        (default: 0.05)
  -c PATH, --csv PATH   If specified, the output will be formatted as CSV and
                        written to PATH
  -d, --drop-exact      If specified, exact matches will be ommited from the
                        output
```

### Examples

#### Generate a list of redirects

Say your're asking **where to redirect all the urls from *old_sitemap.txt* ?**. Pass it as the first argument like so:

```bash
python map.py old_sitemap.txt new_sitemap.txt
```

#### Adjust ambiguity threshold

To influence the level at which two matches are considered equally good, use the `-t VALUE` argument.

```bash
python map.py -t 0.1 old_sitemap.txt new_sitemap.txt
```

#### Omit exact matches

If the results are used to set up 301 redirects on the new website to catch all traffic arriving at old URLs, exact matches can be omitted. They will be handled by actual pages exisiting on the new site (list2). Use the `-d` flag here.

```bash
python map.py -d old_sitemap.txt new_sitemap.txt
```

#### Save output to CSV file

Specify the output filename with `-c PATH`.

```bash
python map.py -c results.csv old_sitemap.txt new_sitemap.txt
```
