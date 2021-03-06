=======
listmap
=======

Adapted from the ``collections.ChainMap`` class. A ``ListMap`` is a dict-like
object that creates a single, updateable view of a list of dicts or other
mappings.

The underlying list of mappings can be accessed and modified
using the ``maps`` property, and the ``append`` method.

Main differences with ``ChainMap`` objects:

* Lookups search the underlying mappings starting from the **last**
  mapping and going backward in the list of mappings until a key is
  found.
* Lookups search the mappings **from right to left** (starting from the last
  mapping in the list and going backward) until a key is found
* Updates and deletions of keys operate on the **last** mapping in the list
* The ``append(m)`` method appends a new mapping ``m`` to the list
* The ``extend(iterable)`` method extends the mappings by appending
  mappings from `iterable`

Examples
========

These examples are adapted from the
`ChainMap docs
<https://docs.python.org/3/library/collections.html#collections.ChainMap>`_ to
show the differences.
::

   >>> baseline = {'music': 'bach', 'art': 'rembrandt'}
   >>> adjustments = {'art': 'van gogh', 'opera': 'carmen'}
   >>> list(ChainMap(adjustments, baseline))
   ['music', 'art', 'opera']

   >>> list(ListMap(baseline, adjustments))
   ['music', 'art', 'opera']

The iteration order of a ``ListMap`` is the same ordering as a series of
``dict.update()`` calls starting from the **first** mapping in the list::

  >>> combined = baseline.copy()
  >>> combined.update(adjustments)
  >>> list(combined)
  ['music', 'art', 'opera']



Contributing
============

This is an OPEN Source Project so please help out by `reporting bugs <https://github.com/simomarsili/listmap>`_ or forking and opening pull requests when possible.

License
=======

Copyright (c) 2020, Simone Marsili.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
