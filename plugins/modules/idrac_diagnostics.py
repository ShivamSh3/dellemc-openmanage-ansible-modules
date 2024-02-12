#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell OpenManage Ansible Modules
# Version 9.0.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r"""
---
module: idrac_diagnostics
short_description: Run and Export iDRAC diagnostics
version_added: "9.0.0"
description:
  - This module allows you to run and export diagnostics on iDRAC.
extends_documentation_fragment:
  - dellemc.openmanage.idrac_auth_options
options:
  run:
    description:
      - Run the diagnostics job on iDRAC.
      - Run the diagnostics job based on the I(run_mode) and save the report in the internal storage. I(reboot_type) is applicable.
    type: bool
    default: true
  export:
    description:
      - Exports the diagnostics information to the given share.
      - This operation requires I(share_parameters).
    type: bool
    default: true
  run_mode:
    description:
      - This option provides the choices to run the diagnostics.
      - C(express) The express diagnostics runs a test package for each server subsystem. However,
        it does not run the complete set of tests available in the package for each subsystem.
      - C(extended) The extended diagnostics run all available tests in each test package for all subsystems.
      - C(long_run) The long-run diagnostics runs express and extended tests.
    type: str
    choices: [express, extended, long_run]
    default: express
  reboot_type:
    description:
      - This option provides the choice to reboot the host immediately to run the diagnostics.
      - This is applicable when I(run) is C(true).
      - C(force) Forced graceful shutdown signals the operating system to turn off and wait for ten minutes.
        If the operating system does not turn off, the iDRAC power cycles the system.
      - C(graceful) Graceful shutdown waits for the operating system to turn off and wait for the system to restart.
      - C(power_cycle) performs a power cycle for a hard reset on the device.
    type: str
    choices: [force, graceful, power_cycle]
    default: graceful
  scheduled_start_time:
    description:
      - Schedules the job at the specified time.
      - The accepted formats are yyyymmddhhmmss and YYYY-MM-DDThh:mm:ss+HH:MM.
      - This is applicable when I(run) is C(true) and I(reboot_type) is power_cycle.
    type: str
  scheduled_end_time:
    description:
      - Run the diagnostic until the specified end date and end time after the I(scheduled_start_time).
      - The accepted formats are yyyymmddhhmmss and YYYY-MM-DDThh:mm:ss+HH:MM.
      - If the run operation does not complete before the specified end time, then the operation fails.
      - This is applicable when I(run) is C(True) and I(reboot_type) is C(power_cycle).
    type: str
  job_wait:
    description:
      - Provides the option to wait for job completion.
      - This is applicable when I(run) is C(true) and I(reboot_type) is C(power_cycle).
    type: bool
    default: true
  job_wait_timeout:
    description:
      - Time in seconds to wait for job completion.
      - This is applicable when I(job_wait) is C(true).
    type: int
    default: 1200
  share_parameters:
    description:
      - Parameters that are required for the export operation of diagnostics.
      - I(share_parameters) is required when I(export) is C(true).
    type: dict
    suboptions:
      share_type:
        description:
          - Share type of the network share.
          - C(local) uses local path for I(export) operation.
          - C(nfs) uses NFS share for I(export) operation.
          - C(cifs) uses CIFS share for I(export) operation.
          - C(http) uses HTTP share for I(export) operation.
          - C(https) uses HTTPS share for I(export) operation.
        type: str
        choices: [local, nfs, cifs, http, https]
        default: local
      file_name:
        description:
          - Diagnostics file name for I(export) operation.
        type: str
      ip_address:
        description:
          - IP address of the network share.
          - I(ip_address) is required when I(share_type) is C(nfs), C(cifs), C(http) or C(https).
        type: str
      share_name:
        description:
          - Network share or local path of the diagnostics file.
        type: str
      workgroup:
        description:
          - Workgroup of the network share.
          - I(workgroup) is applicable only when I(share_type) is C(cifs).
        type: str
      username:
        description:
          - Username of the network share.
          - I(username) is required when I(share_type) is C(cifs).
        type: str
      password:
        description:
          - Password of the network share.
          - I(password) is required when I(share_type) is C(cifs).
        type: str
      ignore_certificate_warning:
        description:
          - Ignores the certificate warning while connecting to Share and is only applicable when I(share_type) is C(https).
          - C(off) ignores the certificate warning.
          - C(on) does not ignore the certificate warning.
        type: str
        choices: ["off", "on"]
        default: "off"
      proxy_support:
        description:
          - Specifies if proxy support must be used or not.
          - C(off) does not use proxy settings.
          - C(default_proxy) uses the default proxy settings.
          - C(parameters_proxy) uses the specified proxy settings. I(proxy_server) is required when I(proxy_support) is C(parameters_proxy).
          - I(proxy_support) is only applicable when I(share_type) is C(https) or C(https).
        type: str
        choices: ["off", "default_proxy", "parameters_proxy"]
        default: "off"
      proxy_type:
        description:
          - The proxy type of the proxy server.
          - C(http) to select HTTP proxy.
          - C(socks) to select SOCKS proxy.
          - I(proxy_type) is only applicable when I(share_type) is C(https) or C(https) and when I(proxy_support) is C(parameters_proxy).
        type: str
        choices: [http, socks]
        default: http
      proxy_server:
        description:
          - The IP address of the proxy server.
          - I(proxy_server) is required when I(proxy_support) is C(parameters_proxy).
          - I(proxy_server) is only applicable when I(share_type) is C(https) or C(https) and when I(proxy_support) is C(parameters_proxy).
        type: str
      proxy_port:
        description:
          - The port of the proxy server.
          - I(proxy_port) is only applicable when I(share_type) is C(https) or C(https) and when I(proxy_support) is C(parameters_proxy).
        type: int
        default: 80
      proxy_username:
        description:
          - The username of the proxy server.
          - I(proxy_username) is only applicable when I(share_type) is C(https) or C(https) and when I(proxy_support) is C(parameters_proxy).
        type: str
      proxy_password:
        description:
          - The password of the proxy server.
          - I(proxy_password) is only applicable when I(share_type) is C(https) or C(https) and when I(proxy_support) is C(parameters_proxy).
        type: str
  resource_id:
    type: str
    description:
      - Id of the resource.
      - If the value for resource ID is not provided, the module picks the first resource ID available from the list of system resources returned by the iDRAC.
requirements:
  - "python >= 3.9.6"
author:
  - "Shivam Sharma(@ShivamSh3)"
notes:
    - Run this module from a system that has direct access to Dell iDRAC.
    - This module supports only iDRAC9 and above.
    - This module supports IPv4 and IPv6 addresses.
    - This module supports C(check_mode).
    - This module requires Dell Diagnostics firmware package to be present on the server.
    - When I(share_type) is C(local) for I(export) operation, job_details are not displayed.
"""

EXAMPLES = r"""
---
- name: Run and export the diagnostics to local path
  dellemc.openmanage.idrac_diagnostics:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "path/to/ca_file"
    run: true
    export: true
    share_parameters:
      share_type: "local"
      share_path: "/opt/local/diagnostics/"
      file_name: "diagnostics.txt"

- name: Run the diagnostics with power cycle reboot on schedule
  dellemc.openmanage.idrac_diagnostics:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "path/to/ca_file"
    run: true
    export: false
    run_mode: "express"
    reboot_type: "power_cycle"
    scheduled_start_time: 20240101101015

- name: Run and export the diagnostics to HTTPS share
  dellemc.openmanage.idrac_diagnostics:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "path/to/ca_file"
    run: true
    export: true
    share_parameters:
      share_type: "HTTPS"
      ignore_certificate_warning: "on"
      share_name: "/share_path/diagnostics_collection_path"
      ip_address: "192.168.0.2"
      file_name: "diagnostics.txt"

- name: Run and export the diagnostics to NFS share
  dellemc.openmanage.idrac_diagnostics:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "path/to/ca_file"
    run: true
    export: true
    share_parameters:
      share_type: "NFS"
      share_name: "nfsshare/diagnostics_collection_path/"
      ip_address: "192.168.0.3"
      file_name: "diagnostics.txt"

- name: Export the diagnostics to CIFS share
  dellemc.openmanage.idrac_diagnostics:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "path/to/ca_file"
    export: true
    run: false
    share_parameters:
      share_type: "NFS"
      share_name: "/cifsshare/diagnostics_collection_path/"
      ip_address: "192.168.0.4"
      file_name: "diagnostics.txt"

- name: Export the diagnostics to HTTPS share via proxy
  dellemc.openmanage.idrac_diagnostics:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    ca_path: "path/to/ca_file"
    export: true
    run: false
    share_parameters:
      share_type: "HTTPS"
      share_name: "/share_path/diagnostics_collection_path"
      ignore_certificate_warning: "on"
      ip_address: "192.168.0.2"
      file_name: "diagnostics.txt"
      proxy_support: parameters_proxy
      proxy_type: http
      proxy_server: "192.168.0.5"
      proxy_port: 1080
      proxy_username: "proxy_user"
      proxy_password: "proxy_password"
"""

RETURN = r'''
---
msg:
  type: str
  description: Status of the diagnostics operation.
  returned: always
  sample: "Successfully run and exported the diagnostics."
job_details:
    description: Returns the output for status of the job.
    returned: For import and export operations
    type: dict
    sample: {
        "ActualRunningStartTime": "2024-01-10T10:14:31",
        "ActualRunningStopTime": "2024-01-10T10:26:34",
        "CompletionTime": "2024-01-10T10:26:34",
        "Description": "Job Instance",
        "EndTime": "2024-01-10T10:30:15",
        "Id": "JID_XXXXXXXXXXXX",
        "JobState": "Completed",
        "JobType": "RemoteDiagnostics",
        "Message": "Job completed successfully.",
        "MessageArgs": [],
        "MessageArgs@odata.count": 0,
        "MessageId": "SYS018",
        "Name": "Remote Diagnostics",
        "PercentComplete": 100,
        "StartTime": "2024-01-10T10:12:15",
        "TargetSettingsURI": null
    }
error_info:
  description: Details of the HTTP Error.
  returned: on HTTP error
  type: dict
  sample: {
    "error": {
      "code": "Base.1.12.GeneralError",
      "message": "A general error has occurred. See ExtendedInfo for more information.",
      "@Message.ExtendedInfo": [
        {
          "Message": "A Remote Diagnostic (ePSA) job already exists.",
          "MessageArgs": [],
          "MessageArgs@odata.count": 0,
          "MessageId": "IDRAC.2.9.SYS098",
          "RelatedProperties": [],
          "RelatedProperties@odata.count": 0,
          "Resolution": "A response action is not required if the scheduled start time of the existing Remote Diagnostic (ePSA) job is ok.
           Else, delete the existing Diagnostics (ePSA) job and recreate another with an appropriate start time.",
          "Severity": "Informational"
        }
      ]
    }
  }
'''

import json
import os
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_redfish import iDRACRedfishAPI, idrac_auth_params
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError
from ansible_collections.dellemc.openmanage.plugins.module_utils.utils import (
    get_current_time, get_dynamic_uri, validate_and_get_first_resource_id_uri, remove_key, idrac_redfish_job_tracking)
from datetime import datetime

MANAGERS_URI = "/redfish/v1/Managers"

OEM = "Oem"
MANUFACTURER = "Dell"
JOBS = "Jobs"
JOBS_EXPAND = "?$expand=*($levels=1)"
LC_SERVICE = "DellLCService"
ACTIONS = "Actions"
EXPORT = "#DellLCService.ExportePSADiagnosticsResult"
RUN = "#DellLCService.RunePSADiagnostics"
ODATA_REGEX = "(.*?)@odata"
ODATA = "@odata.id"
TIME_FORMAT_FILE = "%Y%m%d_%H%M%S"
TIME_FORMAT_WITHOUT_OFFSET = "%Y%m%d%H%M%S"
TIME_FORMAT_WITH_OFFSET = "%Y-%m-%dT%H:%M:%S%z"
SUCCESS_EXPORT_MSG = "Successfully exported the diagnostics."
SUCCESS_RUN_MSG = "Successfully run the diagnostics operation."
SUCCESS_RUN_AND_EXPORT_MSG = "Successfully run and exported the diagnostics."
RUNNING_RUN_MSG = "Successfully triggered the job to run diagnostics."
ALREADY_RUN_MSG = "The diagnostics job is already present."
INVALID_FILE_MSG = "File extension is invalid. Supported extension is: .txt."
INVALID_DIRECTORY_MSG = "Provided directory path '{path}' is not valid."
NO_OPERATION_SKIP_MSG = "Task is skipped as none of run, export or run and export is specified."
INSUFFICIENT_DIRECTORY_PERMISSION_MSG = "Provided directory path '{path}' is not writable. " \
                                        "Please check if the directory has appropriate permissions"
UNSUPPORTED_FIRMWARE_MSG = "iDRAC firmware version is not supported."
TIMEOUT_NEGATIVE_OR_ZERO_MSG = "The parameter `job_wait_timeout` value cannot be negative or zero."
WAIT_TIMEOUT_MSG = "The job is not complete after {0} seconds."
START_TIME = "The specified scheduled start time occurs in the past, " \
             "provide a future time to schedule the start time."
INVALID_TIME = "The specified date and time `{0}` to schedule the diagnostics is not valid. Enter a valid date and time."
END_START_TIME = "The end time `{0}` to schedule the diagnostics must be greater than the start time `{1}`."
NO_CHANGES_FOUND_MSG = "No changes found to be applied."
CHANGES_FOUND_MSG = "Changes found to be applied."

PROXY_SUPPORT = {"off": "Off", "default_proxy": "DefaultProxy", "parameters_proxy": "ParametersProxy"}


class RunDiagnostics:
    STATUS_SUCCESS = [200, 202]

    def __init__(self, idrac, module):
        self.idrac = idrac
        self.module = module
        self.run_url = None

    def execute(self):
        self.__get_run_diagnostics_url()
        self.check_diagnostics_jobs()
        run_diagnostics_status = self.__run_diagnostics()
        job_status = self.__perform_job_wait(run_diagnostics_status)
        status = run_diagnostics_status.status_code
        if status in self.STATUS_SUCCESS and job_status.get('JobState') == "Completed":
            msg = SUCCESS_RUN_MSG
            job_details = job_status
            return msg, job_details
        if status in self.STATUS_SUCCESS and job_status.get('JobState') in ["Scheduled", "Running", "New"]:
            msg = RUNNING_RUN_MSG
            job_details = job_status
            return msg, job_details

    def __run_diagnostics(self):
        reboot_job_types = {
            "graceful": "GracefulRebootWithoutForcedShutdown",
            "force": "GracefulRebootWithForcedShutdown",
            "power_cycle": "PowerCycle"
        }
        run_modes = {
            "express": "Express",
            "extended": "Extended",
            "long_run": "ExpressAndExtended"
        }
        payload = {}
        reboot_type = self.module.params.get('reboot_type')
        run_mode = self.module.params.get('run_mode')
        if reboot_type == "power_cycle":
            if self.module.params.get('scheduled_start_time'):
                start_time = self.__validate_time_format(self.module.params.get('scheduled_start_time'))
                if self.__validate_time(start_time):
                    payload["ScheduledStartTime"] = start_time
            if self.module.params.get('scheduled_end_time'):
                end_time = self.__validate_time_format(self.module.params.get('scheduled_end_time'))
                if self.__validate_time(end_time) and self.__validate_end_time(start_time, end_time):
                    payload["UntilTime"] = end_time
        payload["RebootJobType"] = reboot_job_types.get(reboot_type)
        payload["RunMode"] = run_modes.get(run_mode)
        run_diagnostics_status = self.idrac.invoke_request(self.run_url, "POST", data=payload)
        return run_diagnostics_status

    def __get_run_diagnostics_url(self):
        uri, error_msg = validate_and_get_first_resource_id_uri(
            self.module, self.idrac, MANAGERS_URI)
        if error_msg:
            self.module.exit_json(msg=error_msg, failed=True)
        resp = get_dynamic_uri(self.idrac, uri)
        url = resp.get('Links', {}).get(OEM, {}).get(MANUFACTURER, {}).get(LC_SERVICE, {}).get(ODATA, {})
        if url:
            action_resp = get_dynamic_uri(self.idrac, url)
            run_url = action_resp.get(ACTIONS, {}).get(RUN, {}).get('target', {})
            self.run_url = run_url
        else:
            self.module.exit_json(msg=UNSUPPORTED_FIRMWARE_MSG, failed=True)

    def __validate_job_timeout(self):
        if self.module.params.get("job_wait") and self.module.params.get("job_wait_timeout") <= 0:
            self.module.exit_json(msg=TIMEOUT_NEGATIVE_OR_ZERO_MSG, failed=True)

    def __perform_job_wait(self, run_diagnostics_status):
        job_dict = {}
        job_wait = self.module.params.get('job_wait')
        job_wait_timeout = self.module.params.get('job_wait_timeout')
        self.__validate_job_timeout()
        job_tracking_uri = run_diagnostics_status.headers.get("Location")
        if job_tracking_uri:
            job_id = job_tracking_uri.split("/")[-1]
            res_uri = validate_and_get_first_resource_id_uri(self.module, self.idrac, MANAGERS_URI)
            job_uri = f"{res_uri[0]}/{OEM}/{MANUFACTURER}/{JOBS}/{job_id}"
            if job_wait:
                job_failed, msg, job_dict, wait_time = idrac_redfish_job_tracking(self.idrac, job_uri,
                                                                                  max_job_wait_sec=job_wait_timeout,
                                                                                  sleep_interval_secs=1)
                job_dict = remove_key(job_dict, regex_pattern=ODATA_REGEX)
                if int(wait_time) >= int(job_wait_timeout):
                    self.module.exit_json(msg=WAIT_TIMEOUT_MSG.format(
                        job_wait_timeout), changed=True, job_status=job_dict)
                if job_failed:
                    self.module.fail_json(
                        msg=job_dict.get("Message"), job_status=job_dict)
            else:
                job_resp = self.idrac.invoke_request(job_uri, 'GET')
                job_dict = job_resp.json_data
                job_dict = remove_key(job_dict, regex_pattern=ODATA_REGEX)
        return job_dict

    def __validate_time_format(self, time):
        try:
            datetime_obj = datetime.strptime(time, TIME_FORMAT_WITH_OFFSET)
        except ValueError:
            try:
                datetime_obj = datetime.strptime(time, TIME_FORMAT_WITHOUT_OFFSET)
            except ValueError:
                self.module.exit_json(failed=True, msg=INVALID_TIME.format(time))
        if datetime_obj:
            formatted_time = datetime_obj.strftime(TIME_FORMAT_WITHOUT_OFFSET)
        return formatted_time

    def __validate_time(self, time):
        curr_idrac_time, offset = get_current_time(self.idrac)
        curr_idrac_time = datetime.strptime(curr_idrac_time, TIME_FORMAT_WITH_OFFSET)
        curr_idrac_time = curr_idrac_time.strftime(TIME_FORMAT_WITHOUT_OFFSET)
        currtime_obj = datetime.strptime(curr_idrac_time, TIME_FORMAT_WITHOUT_OFFSET)
        starttime_obj = datetime.strptime(time, TIME_FORMAT_WITHOUT_OFFSET)
        if starttime_obj < currtime_obj:
            self.module.exit_json(failed=True, msg=START_TIME)
        return True

    def __validate_end_time(self, start_time, end_time):
        starttime_obj = datetime.strptime(start_time, TIME_FORMAT_WITHOUT_OFFSET)
        endtime_obj = datetime.strptime(end_time, TIME_FORMAT_WITHOUT_OFFSET)
        if starttime_obj > endtime_obj:
            self.module.exit_json(failed=True, msg=END_START_TIME.format(end_time, start_time))
        return True

    def check_diagnostics_jobs(self):
        res_uri = validate_and_get_first_resource_id_uri(self.module, self.idrac, MANAGERS_URI)
        job_uri = f"{res_uri[0]}/{OEM}/{MANUFACTURER}/{JOBS}{JOBS_EXPAND}"
        job_resp = self.idrac.invoke_request(job_uri, "GET")
        job_list = job_resp.json_data.get('Members', [])
        job_id = ""
        for jb in job_list:
            if jb.get("JobType") == "RemoteDiagnostics" and jb.get("JobState") in ["Scheduled", "Running", "Starting", "New"]:
                job_id = jb['Id']
                job_uri = f"{res_uri[0]}/{OEM}/{MANUFACTURER}/{JOBS}/{job_id}"
                job_details = self.idrac.invoke_request(job_uri, "GET")
                job_dict = remove_key(job_details.json_data, regex_pattern=ODATA_REGEX)
                break
        if self.module.check_mode and job_id:
            self.module.exit_json(msg=NO_CHANGES_FOUND_MSG)
        if self.module.check_mode and not job_id:
            self.module.exit_json(msg=CHANGES_FOUND_MSG, changed=True)
        if job_id:
            self.module.exit_json(msg=ALREADY_RUN_MSG, job_details=job_dict, skipped=True)


class ExportDiagnostics:
    STATUS_SUCCESS = [200, 202]

    def __init__(self, idrac, module):
        self.idrac = idrac
        self.module = module
        self.export_url = None

    def execute(self):
        self.__get_export_diagnostics_url()
        if self.module.check_mode:
            self.perform_check_mode()
        job_status = {}
        self.__check_file_extension()
        share_type = self.module.params.get('share_parameters').get('share_type')
        share_type_methods = {
            "local": self.__export_diagnostics_local,
            "http": self.__export_diagnostics_http,
            "https": self.__export_diagnostics_http,
            "cifs": self.__export_diagnostics_cifs,
            "nfs": self.__export_diagnostics_nfs
        }
        export_diagnostics_status = share_type_methods[share_type]()
        if share_type_methods[share_type] != self.__export_diagnostics_local:
            job_status = self.get_job_status(export_diagnostics_status)
        status = export_diagnostics_status.status_code
        if status in self.STATUS_SUCCESS:
            msg = SUCCESS_EXPORT_MSG
            job_details = job_status
            return msg, job_details

    def __export_diagnostics_local(self):
        payload = {}
        payload["ShareType"] = "Local"
        path = self.module.params.get('share_parameters').get('share_name')
        if not (os.path.exists(path)):
            self.module.fail_json(msg=INVALID_DIRECTORY_MSG.format(path=path))
        if not os.access(path, os.W_OK):
            self.module.fail_json(msg=INSUFFICIENT_DIRECTORY_PERMISSION_MSG.format(path=path))
        diagnostics_status = self.__export_diagnostics(payload)
        diagnostics_file_name = payload.get("FileName")
        diagnostics_data = self.idrac.invoke_request(diagnostics_status.headers.get("Location"), "GET")
        diagnostics_output = [line + "\n" for line in diagnostics_data.body.decode().split("\r\n")]
        file_name = os.path.join(path, diagnostics_file_name)
        with open(file_name, "w") as fp:
            fp.writelines(diagnostics_output)
        return diagnostics_status

    def __export_diagnostics_http(self):
        payload = self.get_payload_details()
        export_status = self.__export_diagnostics(payload)
        return export_status

    def __export_diagnostics_cifs(self):
        payload = self.get_payload_details()
        if self.module.params.get('share_parameters').get('workgroup'):
            payload["Workgroup"] = self.module.params.get('share_parameters').get('workgroup')
        export_status = self.__export_diagnostics(payload)
        return export_status

    def __export_diagnostics_nfs(self):
        payload = self.get_payload_details()
        del payload["UserName"], payload["Password"]
        export_status = self.__export_diagnostics(payload)
        return export_status

    def __get_export_diagnostics_url(self):
        uri, error_msg = validate_and_get_first_resource_id_uri(
            self.module, self.idrac, MANAGERS_URI)
        if error_msg:
            self.module.exit_json(msg=error_msg, failed=True)
        resp = get_dynamic_uri(self.idrac, uri)
        url = resp.get('Links', {}).get(OEM, {}).get(MANUFACTURER, {}).get(LC_SERVICE, {}).get(ODATA, {})
        if url:
            action_resp = get_dynamic_uri(self.idrac, url)
            export_url = action_resp.get(ACTIONS, {}).get(EXPORT, {}).get('target', {})
            self.export_url = export_url
        else:
            self.module.exit_json(msg=UNSUPPORTED_FIRMWARE_MSG, failed=True)

    def __export_diagnostics(self, payload):
        diagnostics_file_name = self.module.params.get('share_parameters').get('file_name')
        if not diagnostics_file_name:
            now = datetime.now()
            hostname = self.module.params.get('idrac_ip')
            diagnostics_file_name = f"{hostname}_{now.strftime(TIME_FORMAT_FILE)}.txt"
        payload["FileName"] = diagnostics_file_name
        diagnostics_status = self.idrac.invoke_request(self.export_url, "POST", data=payload)
        return diagnostics_status

    def __check_file_extension(self):
        file_name = self.module.params.get('share_parameters').get('file_name')
        if file_name:
            file_extension = file_name.lower().endswith(".txt")
            if not file_extension:
                self.module.exit_json(msg=INVALID_FILE_MSG, failed=True)

    def get_job_status(self, export_diagnostics_status):
        res_uri = validate_and_get_first_resource_id_uri(self.module, self.idrac, MANAGERS_URI)
        job_tracking_uri = export_diagnostics_status.headers.get("Location")
        job_id = job_tracking_uri.split("/")[-1]
        job_uri = f"{res_uri[0]}/{OEM}/{MANUFACTURER}/{JOBS}/{job_id}"
        job_failed, msg, job_dict, wait_time = idrac_redfish_job_tracking(self.idrac, job_uri)
        job_dict = remove_key(job_dict, regex_pattern=ODATA_REGEX)
        if job_failed:
            self.module.exit_json(msg=job_dict.get('Message'), failed=True, job_details=job_dict)
        return job_dict

    def get_payload_details(self):
        payload = {}
        payload["ShareType"] = self.module.params.get('share_parameters').get('share_type').upper()
        payload["IPAddress"] = self.module.params.get('share_parameters').get('ip_address')
        payload["ShareName"] = self.module.params.get('share_parameters').get('share_name')
        payload["UserName"] = self.module.params.get('share_parameters').get('username')
        payload["Password"] = self.module.params.get('share_parameters').get('password')
        payload["FileName"] = self.module.params.get('share_parameters').get('file_name')
        payload["IgnoreCertWarning"] = self.module.params.get('share_parameters').get('ignore_certificate_warning').capitalize()
        if self.module.params.get('share_parameters').get('proxy_support') == "parameters_proxy":
            payload["ProxySupport"] = PROXY_SUPPORT[self.module.params.get('share_parameters').get('proxy_support')]
            payload["ProxyType"] = self.module.params.get('share_parameters').get('proxy_type').upper()
            payload["ProxyServer"] = self.module.params.get('share_parameters').get('proxy_server')
            payload["ProxyPort"] = str(self.module.params.get('share_parameters').get('proxy_port'))
            if self.module.params.get('share_parameters').get('proxy_username') and self.module.params.get('share_parameters').get('proxy_password'):
                payload["ProxyUname"] = self.module.params.get('share_parameters').get('proxy_username')
                payload["ProxyPasswd"] = self.module.params.get('share_parameters').get('proxy_password')
        return payload

    def perform_check_mode(self):
        try:
            payload = {}
            payload['ShareType'] = 'Local'
            export_status = self.idrac.invoke_request(self.export_url, "POST", data=payload)
            if export_status.status_code in self.STATUS_SUCCESS:
                self.module.exit_json(msg=CHANGES_FOUND_MSG, changed=True)
        except HTTPError as err:
            filter_err = remove_key(json.load(err), regex_pattern=ODATA_REGEX)
            message_details = filter_err.get('error').get('@Message.ExtendedInfo')[0]
            message_id = message_details.get('MessageId')
            if 'SYS099' in message_id:
                self.module.exit_json(msg=NO_CHANGES_FOUND_MSG)


class RunAndExportDiagnostics:

    def __init__(self, idrac, module):
        self.run = RunDiagnostics(idrac, module)
        self.export = ExportDiagnostics(idrac, module)

    def execute(self):
        msg, job_status = self.run.execute()
        msg, job_status = self.export.execute()
        msg = SUCCESS_RUN_AND_EXPORT_MSG
        return msg, job_status


class Diagnostics:
    _diagnostics_classes = {
        "run": RunDiagnostics,
        "export": ExportDiagnostics,
        "run_and_export": RunAndExportDiagnostics
    }

    @staticmethod
    def diagnostics_operation(idrac, module):
        class_type = None
        if module.params.get("run") and module.params.get("export"):
            class_type = "run_and_export"
        if module.params.get("run"):
            class_type = "run"
        if module.params.get("export"):
            class_type = "export"
        if class_type:
            diagnostics_class = Diagnostics._diagnostics_classes.get(class_type)
            return diagnostics_class(idrac, module)
        else:
            module.exit_json(msg=NO_OPERATION_SKIP_MSG, skipped=True)


def main():
    specs = get_argument_spec()
    specs.update(idrac_auth_params)
    module = AnsibleModule(
        argument_spec=specs,
        required_if=[
            ["run", True, ("reboot_type", "run_mode",)],
            ["export", True, ("share_parameters",)]
        ],
        supports_check_mode=True
    )

    try:
        with iDRACRedfishAPI(module.params) as idrac:
            diagnostics_obj = Diagnostics.diagnostics_operation(idrac, module)
            msg, job_status = diagnostics_obj.execute()
            module.exit_json(msg=msg, changed=True, job_details=job_status)
    except HTTPError as err:
        filter_err = remove_key(json.load(err), regex_pattern=ODATA_REGEX)
        message_details = filter_err.get('error').get('@Message.ExtendedInfo')[0]
        message_id = message_details.get('MessageId')
        if 'SYS099' in message_id:
            module.exit_json(msg=message_details.get('Message'), skipped=True)
        if 'SYS098' in message_id:
            module.exit_json(msg=message_details.get('Message'), skipped=True)
        module.exit_json(msg=str(err), error_info=filter_err, failed=True)
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (ImportError, ValueError, RuntimeError, SSLValidationError,
            ConnectionError, KeyError, TypeError, IndexError) as e:
        module.exit_json(msg=str(e), failed=True)


def get_argument_spec():
    return {
        "run": {"type": 'bool', "default": True},
        "export": {"type": 'bool', "default": True},
        "run_mode": {
            "type": 'str',
            "default": 'express',
            "choices": ['express', 'extended', 'long_run']
        },
        "reboot_type": {
            "type": 'str',
            "default": 'graceful',
            "choices": ['force', 'graceful', 'power_cycle']
        },
        "scheduled_start_time": {"type": 'str'},
        "scheduled_end_time": {"type": 'str'},
        "job_wait": {"type": 'bool', "default": True},
        "job_wait_timeout": {"type": 'int', "default": 1200},
        "share_parameters": {
            "type": 'dict',
            "options": {
                "share_type": {
                    "type": 'str',
                    "default": 'local',
                    "choices": ['local', 'nfs', 'cifs', 'http', 'https']
                },
                "file_name": {"type": 'str'},
                "ip_address": {"type": 'str'},
                "share_name": {"type": 'str'},
                "workgroup": {"type": 'str'},
                "username": {"type": 'str'},
                "password": {"type": 'str', "no_log": True},
                "ignore_certificate_warning": {
                    "type": 'str',
                    "default": "off",
                    "choices": ["off", "on"]
                },
                "proxy_support": {
                    "type": 'str',
                    "default": "off",
                    "choices": ["off", "default_proxy", "parameters_proxy"]
                },
                "proxy_type": {
                    "type": 'str',
                    "default": 'http',
                    "choices": ['http', 'socks']
                },
                "proxy_server": {"type": 'str'},
                "proxy_port": {"type": 'int', "default": 80},
                "proxy_username": {"type": 'str'},
                "proxy_password": {"type": 'str', "no_log": True}
            },
            "required_if": [
                ["share_type", "local", ["share_name"]],
                ["share_type", "nfs", ["ip_address", "share_name"]],
                ["share_type", "cifs", ["ip_address", "share_name", "username", "password"]],
                ["share_type", "http", ["ip_address", "share_name"]],
                ["share_type", "https", ["ip_address", "share_name"]],
                ["proxy_support", "parameters_proxy", ["proxy_server"]]
            ],
            "required_together": [
                ("username", "password"),
                ("proxy_username", "proxy_password")
            ]
        },
        "resource_id": {"type": 'str'}
    }


if __name__ == '__main__':
    main()
