import logging
from ConfigParser import NoSectionError, NoOptionError

def _getMembership(config, user, seen, mode):
    log = logging.getLogger('gitosis.group.getMembership')

    for section in config.sections():
        GROUP_PREFIX = 'group '
        if not section.startswith(GROUP_PREFIX):
            continue
        group = section[len(GROUP_PREFIX):]
        if group in seen:
            continue

        try:
            if mode == 'writable' or mode == 'writeable':
                members = config.get(section, 'members')
            else:
                members = config.get(section, 'readonly')
        except (NoSectionError, NoOptionError):
            members = []
        else:
            members = members.split()

        # @all is the only group where membership needs to be
        # bootstrapped like this, anything else gets started from the
        # username itself
        if (user in members
            or '@all' in members):
            log.debug('found %(user)r in %(mode)r %(group)r' % dict(
                user=user,
                mode=mode,
                group=group,
                ))
            seen.add(group)
            yield group

            for member_of in _getMembership(
                config, '@%s' % group, seen, mode
                ):
                yield member_of


def getMembership(config, user, mode):
    """
    Generate groups ``user`` is member of, according to ``config``

    :type config: RawConfigParser
    :type user: str
    :param _seen: internal use only
    :type mode: str
    """

    seen = set()
    for member_of in _getMembership(config, user, seen, mode):
        yield member_of

    # everyone is always a member of group "all"
    yield 'all'

