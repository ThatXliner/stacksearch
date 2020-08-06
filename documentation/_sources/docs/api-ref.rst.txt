.. _api-ref:

################################
The API Reference
################################

This document will list all available APIs and their documentation.

----------------------------------------------------------------

.. function:: Search(Query [, print_prog = True, search_on_site = "stackoverflow", *args, **kwargs])

   This function is the main "meat" of stacksearch. It will search stackoverflow (or any other StackExchange site specified) for your search query.

   If you want to print the progress (which by default is true), then you can set the argument "print_prog" to "true".

   If you want to search on other StackExchange sites, you can set the argument "search_on" to the URL of the StackExchange site to search (including or excluding the ``.com`` suffix).

.. function:: fSearch(Query [, print_prog = True, search_on_site = "stackoverflow", *args, **kwargs])

   This function is almost identical to the ``Search`` function defined above except that it is *asynchronous*.
