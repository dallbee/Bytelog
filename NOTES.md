## Links
http://kecebongsoft.com
http://splendidabacus.com/martin-pelican/my-super-post.html
http://steveasleep.com

## Articles
- Regular Expressions
- An opinion on when JS should, and shouldn't be used (and how)

## Features
- Twitter Integration
- content as compiled markdown files (tracked via github)
- browserstring page tracking
- custom routes
- syntax highlighting
- metadata parsing
- js for useability (no-js fallbacks)

## Implementation Details

### Content
Git hook -> Git Pull -> Parse Markdown -> Output file.jinja


## URL Schema
/page-name
/projects
/writings
/about

## Pages

``` INDEX
Dylan Allbee
Writings / Projects / About

Thoughts, articles, and tutorials that I have written
with the intent of public exposure. I encourage you to read with an open
mind and discuss.

  This is an approximation        Title of Article - February 6th
  of a thought. From Twitter      Here is a sample description of the article. It
                                  should be fairly short.
  Here is another thought
                                  Another Article - January 31st, 2015
  And a final thought. Perhaps    Yet another description! Should I hard cap the
  I should also share tweets?     character limit?

Copyright © 2015-2016 by Dylan Allbee
```

``` Projects
Mons

Allbee.org
```

``` ABOUT
Some notable life events.

  Oct 2015 - Began working at Index Fund Advisors
  Sep 2015 - Moved to Tustin, CA
  Jun 2015 - Received B.S. in Computer Engineering from CSU San Bernardino
  Jun 2015 - Received B.S. in Applied Physics from CSU San Bernardino
  Jan 2013 - Started as a Computer Science Intern at Optivus Proton Therary
  Jun 2010 - Graduated from Rim of the World High School
  Jul 2002 - Wrote my first C++ program (Tic-tac-toe)
  Dec 1991 - Born in Twin Peaks, CA
```