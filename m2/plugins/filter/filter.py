#!/usr/bin/env python

import re #imports regular expression library

class FilterModule:

    @staticmethod
    def filters():
        return {
                'bgp_as_from_rt': FilterModule.bgp_as_from_rt,
                'ios_vrf_rt': FilterModule.ios_vrf_rt
                }

    @staticmethod
    def bgp_as_from_rt(rt_list):
        bgp_as_list = []
        for my_rt in rt_list:
            rt_halves = my_rt.split(':')
            bgp_as_list.append(int(rt_halves[0]))

        return bgp_as_list

    @staticmethod
    def ios_vrf_rt(text):
        vrf_list = ['vrf' + s for s in text.split('vrf') if s]
        return_dict = {}
        for vrf in vrf_list:
            # Parse the VRF name from the definition line
            # little \s matches spaces
            # '+' = match atleast 1 instance (but match all if there is more)
            # big \S matches every other chacter
            name_regex = re.compile(r'vrf\s+definition\s+(?P<name>\S+)')
            name_match = name_regex.search(vrf)
            sub_dict = {}
            vrf_dict = {name_match.group('name'): sub_dict}

            # Parse the RT imports into a list of strings
            rti_regex = re.compile(r'route-target\s+import\s+(?P<rti>\d+:\d+)')
            rti_matches = rti_regex.findall(vrf)
            sub_dict.update({'route_import': rti_matches})

            # Parse the RT exports into a list of strings
            rte_regex = re.compile(r'route-target\s+export\s+(?P<rte>\d+:\d+)')
            rte_matches = rte_regex.findall(vrf)
            sub_dict.update({'route_export': rte_matches})

            # Append dictionary to return list
            return_dict.update(vrf_dict)


        return return_dict
