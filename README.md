# Description
This repository implements the Github node allowlist of Vultr.

Process:
1. Take IPs of Github services from Github API
2. Update IPs in Vultr's firewall rules<br>
2.1 Delete old IPs<br>
2.2 Add new IPs

# Dependency
pip install requests

# License
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction.

THE SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY.

2023 dittozhang(D1tt0)
