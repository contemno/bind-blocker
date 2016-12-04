# bind-blocker

Just a quick and dirty zone file generator for blocking advertising domains with bind. Simply append an 'include "blocked.conf";' to your named.conf referencing the output file from this generator.

The named process will respond with a NXDOMAIN in response to queries to any RR of the blocked domains and not answer for any lookups of the domains themselves.
