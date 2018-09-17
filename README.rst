Google Visualization API
########################

This project is a helper python library for providers who want to implement a
data source for visualizations built on the
`Google Visualization API <https://code.google.com/apis/visualization/>`_.

- **Documentation** - See the `API documentation
  <https://developers.google.com/chart/interactive/docs/dev/gviz_api_lib>`_
  for details about how to use this library.
- **Installation** - ``pip install gviz_api``
- **Samples** - You can see sample code illustrating how to use the library
  `here <https://github.com/google/google-visualization-python/tree/master/examples/>`_.

..

  (Please note that the dynamic example is not a full html page example but
  rather is an actual data source url that you can plug into a
  google.visualization.Query.
  See documentation at:
  http://code.google.com/apis/visualization/documentation/queries.html)


Pure ASCII
----------
The helper library does its own Unicode escaping by encoding JSON strings in
UTF-8. Alas, the resulting JSON string

- is not usable in a template system like Jinja2 which only accepts pure ASCII
  ``str`` or ``unicode`` strings
- is harder to sanitize to prevent cross site scripting (XSS)
- is unnecessary because Unicode characters can be used in JSON
- is overly complex because JSON can escape Unicode with hexadecimal escapes

This fork outputs pure ASCII JSON strings to eliminate these problems and
ensure maximal interoperability. Unicode code points are encoded with
hexadecimal escapes per `the standard <http://json.org/>`_.

**Why would you embed a JSON string in a template?** Having the JSON string in
a HTML page saves a JSON request to retrieve the data and makes the page load
faster.


Backport
--------
This branch backports the code for use in Python 2.x.


License
-------

Copyright (C) 2009 Google Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
