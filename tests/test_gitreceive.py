def test_gitreceive(Command, Ansible):
    Command('rm -rf /home/git/test /tmp/gitreceive')
    push = Command('git -C /root/gitreceive push test master')
    assert push.rc == 0
    assert 'OK' in push.stderr
    second_push = Command('git -C /root/gitreceive push test master')
    assert second_push.rc == 0
    assert 'Everything up-to-date' == second_push.stderr
