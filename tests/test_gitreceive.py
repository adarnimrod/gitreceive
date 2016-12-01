from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')


def test_gitreceive(Command, Sudo):
    with Sudo():
        Command('rm -rf /home/git/test /var/tmp/gitreceive')
        push = Command('git -C /root/gitreceive push test master')
    assert push.rc == 0
    assert 'OK' in push.stderr
    with Sudo():
        second_push = Command('git -C /root/gitreceive push test master')
    assert second_push.rc == 0
    assert 'Everything up-to-date' in second_push.stderr
