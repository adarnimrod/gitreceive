from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')


def test_gitreceive(Command, Sudo):
    with Sudo():
        Command('rm -rf /home/git/test /var/tmp/gitreceive')
        push = Command('git -C /root/gitreceive-test push test master')
    assert push.rc == 0
    for message in ['----> Unpacking ...', '----> Fetching submodules ...',
                    '----> Running receiver ...', 'Dummy receiver script',
                    '----> Cleanup ...', '----> OK.']:
        assert message in push.stderr
    with Sudo():
        second_push = Command('git -C /root/gitreceive-test push test master')
    assert second_push.rc == 0
    assert 'Everything up-to-date' in second_push.stderr
