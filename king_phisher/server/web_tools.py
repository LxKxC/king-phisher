#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  king_phisher/server/web_tools.py
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following disclaimer
#    in the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of the project nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import os

import smoke_zephyr.utilities

def get_hostnames(config):
	"""
	List the hostnames that are configured for this server instance. This list
	is generated by first checking the server's configuration for the
	``hostnames`` option. Then if ``vhost_directories`` is enabled, the webroot
	is checked for additional values.

	.. note::
		This function makes no attempt to validate these values, they are
		strictly what have been configured for use.

	.. versionadded:: 1.13.0

	:param config: Configuration to retrieve settings from.
	:type config: :py:class:`smoke_zephyr.configuration.Configuration`
	:return: A tuple of the enumerated hostnames.
	:rtype: tuple
	"""
	hostnames = config.get_if_exists('server.hostnames', [])
	hostnames.extend(get_vhost_directories(config) or ())
	hostnames = smoke_zephyr.utilities.unique(hostnames)
	return tuple(sorted(hostnames))

def get_vhost_directories(config):
	"""
	List the hostnames that are configured through the Virtual Host directories.
	If the server option ``vhost_directories`` is disabled, this function
	returns ``None``.

	.. versionadded:: 1.13.0

	:param config: Configuration to retrieve settings from.
	:type config: :py:class:`smoke_zephyr.configuration.Configuration`
	:return: A tuple of the enumerated virtual hostname directories.
	:rtype: tuple
	"""
	if not config.get('server.vhost_directories'):
		return None
	web_root = config.get('server.web_root')
	directories = [entry for entry in os.listdir(web_root) if os.path.isdir(os.path.join(web_root, entry))]
	return tuple(sorted(directories))