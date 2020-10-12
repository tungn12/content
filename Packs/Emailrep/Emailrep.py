"""HelloWorld Integration for Cortex XSOAR (aka Demisto)

This integration is a good example on you can build a Cortex XSOAR Integration
using Python 3. Please follow the documentation links below and make sure that
your integration follows the Code Conventions and passes the Linting phase.

Developer Documentation: https://xsoar.pan.dev/docs/welcome
Code Conventions: https://xsoar.pan.dev/docs/integrations/code-conventions
Linting: https://xsoar.pan.dev/docs/integrations/linting

When building a Cortex XSOAR integration that is reusable, a lot of effort
must be placed in the design. We recommend to fill a Design Document template,
that allows you to capture Use Cases, Requirements and Inputs/Outputs.

Example Design document for the this Integration (HelloWorld):
https://docs.google.com/document/d/1wETtBEKg37PHNU8tYeB56M1LE314ux086z3HFeF_cX0


HelloWorld API
--------------

The HelloWorld API is a simple API that shows a realistic use case for an XSOAR
integration. It's actually a real API that is available to the following URL:
https://soar.mastersofhack.com - if you need an API Key to test it out please
reach out to your Cortex XSOAR contacts.

This API has a few basic functions:
- Alerts: the endpoint returns mocked alerts and allows you to search based on
a number of parameters, such as state (ACTIVE or CLOSED), type, timestamp. It
can also return a single alert by ID. This is used to create new Incidents in
XSOAR by using the ``fetch-incidents`` command, which is by default invoked
every minute.
There is also an endpoint that allows to retrieve additional details about a
specific alert by ID, and one to change the alert status to "CLOSED" once
it has been resolved.

- Reputation (ip and domain): these endpoints return, for an IP and
domain respectively, a WHOIS lookup of the entity as well as a reputation score
(from 0 to 100) that is used to determine whether the entity is malicious. This
endpoint is called by XSOAR reputation commands ``ip`` and ``domain`` that
are run automatically every time an indicator is extracted in XSOAR. As a best
practice of design, it is important to map and document the mapping between
a score in the original API format (0 to 100 in this case) to a score in XSOAR
format (0 to 3). This score is called ``DBotScore``, and is returned in the
context to allow automated handling of indicators based on their reputation.
More information: https://xsoar.pan.dev/docs/integrations/dbot


- Scan: to demonstrate how to run commands that are not returning instant data,
the API provides a scan endpoint that simulates scanning a host and generating
a report after the scan is completed. The API has endpoints to start a scan,
which returns a job ID, poll for the scan status and, if the scan is completed,
retrieved the job results.
This function is used in conjunction of the HelloWorld Scan playbook that uses
the GenericPolling mechanism to implement the job polling loop. The results
can be returned in JSON or attachment file format.
Info on GenericPolling: https://xsoar.pan.dev/docs/playbooks/generic-polling

Please check the HelloWorld Design Document referenced above for details about
the raw API responsens as well as the design details for this integration.

This integration also has a ``say-hello`` command for backward compatibility,
that doesn't connect to an API and just returns a ``Hello {name}`` string,
where name is the input value provided.


Integration File Structure
--------------------------

An integration usually consists of the following parts:
- Imports
- Constants
- Client Class
- Helper Functions
- Command Functions
- Main Function
- Entry Point


Imports
-------

Here you can import Python module you need for your integration. If you need
a module that is not part of the default XSOAR Docker images, you can add
a custom one. More details: https://xsoar.pan.dev/docs/integrations/docker

There are also internal imports that are used by XSOAR:
- demistomock (imported as demisto): allows your code to work offline for
testing. The actual ``demisto`` module is provided at runtime when the
code runs in XSOAR.
- CommonServerPython.py: contains a set of helper functions, base classes
and other useful components that will make your integration code easier
to maintain.
- CommonServerUserPython.py: includes a set of user defined commands that
are specific to an XSOAR installation. Do not use it for integrations that
are meant to be shared externally.

These imports are automatically loaded at runtime within the XSOAR script
runner, so you shouldn't modify them

Constants
---------

Usually some constants that do not require user parameters or inputs, such
as the default API entry point for your service, or the maximum numbers of
incidents to fetch every time.


Client Class
------------

We recommend to use a Client class to wrap all the code that needs to interact
with your API. Moreover, we recommend, when possible, to inherit from the
BaseClient class, defined in CommonServerPython.py. This class already handles
a lot of the work, such as system proxy settings, SSL certificate verification
and exception handling for HTTP errors.

Note that the Client class should NOT contain any Cortex XSOAR specific code,
i.e. it shouldn't use anything in the ``demisto`` class (functions such as
``demisto.args()`` or ``demisto.results()`` or even ``return_results`` and
``return_error``.
You will use the Command Functions to handle XSOAR inputs and outputs.

When calling an API, you should use the ``_http.request()`` method and you
can return the raw data to the calling function (usually a Command function).

You should usually have one function for each API endpoint.

Look at the code and the commends of this specific class to better understand
the implementation details.


Helper Functions
----------------

Helper functions are usually used as utility functions that are used by several
command functions throughout your code. For example they map arguments to types
or convert severity formats from integration-specific to XSOAR.
Many helper functions are already defined in ``CommonServerPython.py`` and are
often very handy.


Command Functions
-----------------

Command functions perform the mapping between XSOAR inputs and outputs to the
Client class functions inputs and outputs. As a best practice, they shouldn't
contain calls to ``demisto.args()``, ``demisto.results()``, ``return_error``
and ``demisto.command()`` as those should be handled through the ``main()``
function.
However, in command functions, use ``demisto`` or ``CommonServerPython.py``
artifacts, such as ``demisto.debug()`` or the ``CommandResults`` class and the
``Common.*`` classes.
Usually you will have one command function for every specific XSOAR command
you want to implement in your integration, plus ``test-module``,
``fetch-incidents`` and ``fetch-indicators``(if the latter two are supported
by your integration). Each command function should invoke one specific function
of the Client class.

Command functions, when invoked through an XSOAR command usually return data
using the ``CommandResults`` class, that is then passed to ``return_results()``
in the ``main()`` function.
``return_results()`` is defined in ``CommonServerPython.py`` to return
the data to XSOAR. ``return_results()`` actually wraps ``demisto.results()``.
You should never use ``demisto.results()`` directly.

Sometimes you will need to return values in a format that is not compatible
with ``CommandResults`` (for example files): in that case you must return a
data structure that is then pass passed to ``return.results()``. (i.e.
check the ``scan_results_command`` function in this file that has the option
to return a file to Cortex XSOAR).

In any case you should never call ``return_results()`` directly from the
command functions.

When you use create the CommandResults object in command functions, you
usually pass some types of data:

- Human Readable: usually in Markdown format. This is what is presented to the
analyst in the War Room. You can use ``tableToMarkdown()``, defined in
``CommonServerPython.py``, to convert lists and dicts in Markdown and pass it
to ``return_results()`` using the ``readable_output`` argument, or the
``return_results()`` function will call ``tableToMarkdown()`` automatically for
you.

- Context Output: this is the machine readable data, JSON based, that XSOAR can
parse and manage in the Playbooks or Incident's War Room. The Context Output
fields should be defined in your integration YML file and is important during
the design phase. Make sure you define the format and follow best practices.
You can use ``demisto-sdk json-to-outputs`` to autogenerate the YML file
outputs section. Context output is passed as the ``outputs`` argument in ``demisto_results()``,
and the prefix (i.e. ``HelloWorld.Alert``) is passed via the ``outputs_prefix``
argument.

More information on Context Outputs, Standards, DBotScore and demisto-sdk:
https://xsoar.pan.dev/docs/integrations/code-conventions#outputs
https://xsoar.pan.dev/docs/integrations/context-and-outputs
https://xsoar.pan.dev/docs/integrations/context-standards
https://xsoar.pan.dev/docs/integrations/dbot
https://github.com/demisto/demisto-sdk/blob/master/demisto_sdk/commands/json_to_outputs/README.md

Also, when you write data in the Context, you want to make sure that if you
return updated information for an entity, to update it and not append to
the list of entities (i.e. in HelloWorld you want to update the status of an
existing ``HelloWorld.Alert`` in the context when you retrieve it, rather than
adding a new one if you already retrieved it). To update data in the Context,
you can define which is the key attribute to use, such as (using the example):
``outputs_key_field='alert_id'``. This means that you are using the ``alert_id``
key to determine whether adding a new entry in the context or updating an
existing one that has the same ID. You can look at the examples to understand
how it works.
More information here:
https://xsoar.pan.dev/docs/integrations/context-and-outputs
https://xsoar.pan.dev/docs/integrations/code-conventions#outputs
https://xsoar.pan.dev/docs/integrations/dt

- Raw Output: this is usually the raw result from your API and is used for
troubleshooting purposes or for invoking your command from Automation Scripts.
If not specified, ``return_results()`` will use the same data as ``outputs``.


Main Function
-------------

The ``main()`` function takes care of reading the integration parameters via
the ``demisto.params()`` function, initializes the Client class and checks the
different options provided to ``demisto.commands()``, to invoke the correct
command function passing to it ``demisto.args()`` and returning the data to
``return_results()``. If implemented, ``main()`` also invokes the function
``fetch_incidents()``with the right parameters and passes the outputs to the
``demisto.incidents()`` function. ``main()`` also catches exceptions and
returns an error message via ``return_error()``.


Entry Point
-----------

This is the integration code entry point. It checks whether the ``__name__``
variable is ``__main__`` , ``__builtin__`` (for Python 2) or ``builtins`` (for
Python 3) and then calls the ``main()`` function. Just keep this convention.

"""
import demistomock as demisto
from CommonServerPython import *
from CommonServerUserPython import *

import urllib3
import traceback
from typing import Any, Dict, List, Optional

# Disable insecure warnings
#from CommonServerPython import DBotScoreType

urllib3.disable_warnings()


''' CONSTANTS '''


#DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
ACCEPTED_TAGS = ['account_takeover', 'bec', 'brand_impersonation', 'browser_exploit', 'credential_phishing',
                 'generic_phishing', 'malware', 'scam', 'spam', 'spoofed', 'task_request', 'threat_actor']

''' CLIENT CLASS '''


class Client(BaseClient):
    """Client class to interact with the service API

    This Client implements API calls, and does not contain any Demisto logic.
    Should only do requests and return data.
    It inherits from BaseClient defined in CommonServer Python.
    Most calls use _http_request() that handles proxy, SSL verification, etc.
    For this HelloWorld implementation, no special attributes defined
    """

    def get_email_address_reputation(self, email: str) -> Dict[str, Any]:
        """Gets the IP reputation using the '/{email}' API endpoint

        :type email: ``str``
        :param ip: email address to get the reputation for

        :return: dict containing the email reputation as returned from the API
        :rtype: ``Dict[str, Any]``
        """

        return self._http_request(
            method='GET',
            url_suffix=f"/{email}"
        )

    def post_email_address_report(self, email: str, tags: List[str], description: Optional[str],
                                  timestamp: Optional[int], expires: Optional[int]) -> Dict[str, Any]:
        """Gets the IP reputation using the '/{email}' API endpoint

        :type email: ``str``
        :param ip: email address to get the reputation for

        :return: dict containing the email reputation as returned from the API
        :rtype: ``Dict[str, Any]``
        """
        request_params: Dict[str, Any] = {}
        request_params['email'] = email
        request_params['tags'] = tags

        if description:
            request_params['description'] = description

        if timestamp:
            request_params['timestamp'] = timestamp

        if expires:
            request_params['expires'] = expires

        return self._http_request(
            method='POST',
            url_suffix='/report',
            params=request_params
        )


''' COMMAND FUNCTIONS '''


def test_module(client: Client, first_fetch_time: int) -> str:
    """Tests API connectivity and authentication'

    Returning 'ok' indicates that the integration works like it is supposed to.
    Connection to the service is successful.
    Raises exceptions if something goes wrong.

    :type client: ``Client``
    :param Client: HelloWorld client to use

    :type name: ``str``
    :param name: name to append to the 'Hello' string

    :return: 'ok' if test passed, anything else will fail the test.
    :rtype: ``str``
    """

    # INTEGRATION DEVELOPER TIP
    # Client class should raise the exceptions, but if the test fails
    # the exception text is printed to the Cortex XSOAR UI.
    # If you have some specific errors you want to capture (i.e. auth failure)
    # you should catch the exception here and return a string with a more
    # readable output (for example return 'Authentication Error, API Key
    # invalid').
    # Cortex XSOAR will print everything you return different than 'ok' as
    # an error
    try:
        client.search_alerts(max_results=1, start_time=first_fetch_time, alert_status=None, alert_type=None, severity=None)
    except DemistoException as e:
        if 'Forbidden' in str(e):
            return 'Authorization Error: make sure API Key is correctly set'
        else:
            raise e
    return 'ok'


def email_command(client: Client, args: Dict[str, Any]) -> CommandResults:
    """TODO: rewrite this
    ip command: Returns IP reputation for a list of IPs

    :type client: ``Client``
    :param Client: HelloWorld client to use

    :type args: ``Dict[str, Any]``
    :param args:
        all command arguments, usually passed from ``demisto.args()``.
        ``args['ip']`` is a list of IPs or a single IP
        ``args['threshold']`` threshold to determine whether an IP is malicious

    :type default_threshold: ``int``
    :param default_threshold:
        default threshold to determine whether an IP is malicious
        if threshold is not specified in the XSOAR arguments

    :return:
        A ``CommandResults`` object that is then passed to ``return_results``,
        that contains IPs

    :rtype: ``CommandResults``
    """

    emails = argToList(args.get('email_address'))
    if len(emails) == 0:
        raise ValueError('Email(s) not specified')

    email_data_list: List[Dict[str, Any]] = []
    email_standard_list: List[Common.EMAIL] = []
    for email in emails:
        email_data = client.get_email_address_reputation(email)
        email_data_list.append(email_data)

        score = Common.DBotScore.NONE
        description = 'EmailRep returned'
        suspicious = email_data.get('suspicious')
        # might cause problems.
        malicious_activity_recent = email_data.get('malicious_activity_recent')
        credentials_leaked_recent = email_data.get('credentials_leaked_recent')
        if not suspicious:
            score = Common.DBotScore.GOOD
            description += ' not suspicious'
        elif malicious_activity_recent or credentials_leaked_recent:
            if malicious_activity_recent:
                description += ' malicious_activity_recent '
            if credentials_leaked_recent:
                description += ' credentials_leaked_recent'
            score = Common.DBotScore.BAD
        else:
            score = Common.DBotScore.SUSPICIOUS

        dbot_score = Common.DBotScore(
            indicator=ip,
            indicator_type=DBotScoreType.EMAIL,
            integration_name='EmailRep',
            score=score,
            malicious_description=description
        )

        email_context = Common.EMAIL(
            emailaddress=email,
            dbot_score=dbot_score
        )
        email_standard_list.append(email_context)

    readable_output = tableToMarkdown('Email List', email_data_list)

    return CommandResults(
        readable_output=readable_output,
        outputs_prefix='EmailRep.EmailScore',
        outputs_key_field='email',
        outputs=email_data_list,
        indicators=email_standard_list
    )


def email_reputation_command(client: Client, args: Dict[str, Any]) -> CommandResults:
    """TODO: rewrite this.
    ip command: Returns IP reputation for a list of IPs

    :type client: ``Client``
    :param Client: HelloWorld client to use

    :type args: ``Dict[str, Any]``
    :param args:
        all command arguments, usually passed from ``demisto.args()``.
        ``args['ip']`` is a list of IPs or a single IP
        ``args['threshold']`` threshold to determine whether an IP is malicious

    :type default_threshold: ``int``
    :param default_threshold:
        default threshold to determine whether an IP is malicious
        if threshold is not specified in the XSOAR arguments

    :return:
        A ``CommandResults`` object that is then passed to ``return_results``,
        that contains IPs

    :rtype: ``CommandResults``
    """

    emails = argToList(args.get('email_address'))
    if len(emails) == 0:
        raise ValueError('Email(s) not specified')

    email_data_list: List[Dict[str, Any]] = []
    for email in emails:
        email_data = client.get_email_address_reputation(email)
        email_data_list.append(email_data)

    readable_output = tableToMarkdown('Email List', email_data_list)

    return CommandResults(
        readable_output=readable_output,
        outputs_prefix='EmailRep.Email',
        outputs_key_field='email',
        outputs=email_data_list
    )

def report_email_address_command(client: Client, args: Dict[str, Any]) -> CommandResults:
    """Report email address to EmailRep

    Args:
        client:
        args:

    Returns:

    """

    email_address = args.get('email_address')
    if email_address == '':
        raise ValueError('Email(s) not specified')
    tags = argToList(args.get('tags'))
    if len(tags) == 0:
        raise ValueError('Tag(s) not specified')
    for tag in tags:
        if tag not in ACCEPTED_TAGS:
            raise ValueError(f'Tag \'{tag}\' not in accepted tag list')
    description = args.get('description')
    timestamp = int(args.get('description'))
    expires = int(args.get('expires'))

    result = client.post_email_address_report(email_address, tags, description, timestamp, expires)

    # Not sure about this. Need to read Common
    readable_output = tableToMarkdown('Email Report Response', result)

    return CommandResults(
        readable_output=readable_output,
        outputs_prefix='EmailRep.Report',
        outputs_key_field='status',
        outputs=result
    )


''' MAIN FUNCTION '''


def main() -> None:
    """main function, parses params and runs command functions

    :return:
    :rtype:
    """

    api_key = demisto.params().get('apikey')

    # get the service API url
    #base_url = urljoin(demisto.params()['url'], '/api/v1')
    base_url = demisto.params()['url']

    # if your Client class inherits from BaseClient, SSL verification is
    # handled out of the box by it, just pass ``verify_certificate`` to
    # the Client constructor
    verify_certificate = not demisto.params().get('insecure', False)

    # if your Client class inherits from BaseClient, system proxy is handled
    # out of the box by it, just pass ``proxy`` to the Client constructor
    proxy = demisto.params().get('proxy', False)

    # INTEGRATION DEVELOPER TIP
    # You can use functions such as ``demisto.debug()``, ``demisto.info()``,
    # etc. to print information in the XSOAR server log. You can set the log
    # level on the server configuration
    # See: https://xsoar.pan.dev/docs/integrations/code-conventions#logging

    demisto.debug(f'Command being called is {demisto.command()}')
    try:
        headers = {
            'Authorization': f'Bearer {api_key}'
        }
        client = Client(
            base_url=base_url,
            verify=verify_certificate,
            headers=headers,
            proxy=proxy)

        if demisto.command() == 'emailrep-email-reputation-get':
            return_results(email_reputation_command(client, demisto.args()))

        elif demisto.command() == 'email':
            return_results(email_command(client, demisto.args()))

        elif demisto.command() == 'emailrep-email-address-report':
            return_results(report_email_address_command(client, demisto.args()))

        elif demisto.command() == 'test-module':
            # This is the call made when pressing the integration Test button.
            result = test_module(client, first_fetch_time)
            return_results(result)


    # Log exceptions and return errors
    except Exception as e:
        demisto.error(traceback.format_exc())  # print the traceback
        return_error(f'Failed to execute {demisto.command()} command.\nError:\n{str(e)}')


''' ENTRY POINT '''


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()