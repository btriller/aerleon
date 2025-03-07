# Copyright 2011 Google Inc. All Rights Reserved.
# Modifications Copyright 2022-2023 Aerleon Project Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Command line interface to aclcheck library."""

import pathlib
from optparse import OptionParser

from aerleon.lib import aclcheck, naming, policy, yaml


def main():
    # TODO(robankeny): Lets move this to gflags
    usage = 'usage: %prog [options] arg'
    _parser = OptionParser(usage)
    _parser.add_option(
        '--definitions-directory',
        dest='definitions',
        help='definitions directory',
        default='./def',
    )
    _parser.add_option(
        '--base-directory',
        dest='basedir',
        help='The base directory to look for include files.',
        default='',
    )
    _parser.add_option(
        '-p',
        '--policy-file',
        dest='pol',
        help='policy file',
        default='./policies/pol/sample_paloalto_yaml.yaml',
    )
    _parser.add_option(
        '-d', '--destination', dest='dst', help='destination IP', default='200.1.1.1'
    )
    _parser.add_option('-s', '--source', dest='src', help='source IP', default='any')
    _parser.add_option(
        '--proto',
        '--protocol',
        dest='proto',
        help='Protocol (tcp, udp, icmp, etc.)',
        default='tcp',
    )
    _parser.add_option(
        '--dport', '--destination-port', dest='dport', help='destination port', default='80'
    )
    _parser.add_option(
        '--sport', '--source-port', dest='sport', help='source port', default='1025'
    )
    (FLAGS, unused_args) = _parser.parse_args()

    defs = naming.Naming(FLAGS.definitions)
    with open(FLAGS.pol) as f:
        conf = f.read()
    if pathlib.Path(FLAGS.pol).suffix in ['.yaml', '.yml']:
        policy_obj = yaml.ParsePolicy(
            conf,
            base_dir=FLAGS.basedir,
            filename=FLAGS.pol,
            definitions=defs,
        )
    else:
        policy_obj = policy.ParsePolicy(conf, defs, base_dir=FLAGS.basedir)
    check = aclcheck.AclCheck(
        policy_obj,
        src=FLAGS.src,
        dst=FLAGS.dst,
        sport=FLAGS.sport,
        dport=FLAGS.dport,
        proto=FLAGS.proto,
    )
    print(str(check))


if __name__ == '__main__':
    main()
