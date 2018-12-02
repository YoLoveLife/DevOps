import yaml, json
st = """
tasks:
    - name: filetest
      copy: src=file:{{WAR}} dest=/usr/local/tmp.war
    - name: touch
      shell: touch /tmp/ddr
    - name: fileddr
      copy: src=file:{{HOSTS}} dest=/etc/hosts
    - name: ddr
      copy: src=file:{{BGM}} dest=/tmp/bgm
"""
