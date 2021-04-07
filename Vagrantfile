#e -*- mode: ruby -*-
## vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"
VAGRANTFILE_LOCAL = 'Vagrantfile.local'

# virtualenv setup reference: https://wwken.wordpress.com/2015/05/02/how-to-change-default-python-version-in-ubuntu-using-virtualenv/

$script = <<SCRIPT
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y gcc-multilib g++-multilib libffi-dev libffi6 libffi6-dbg python-crypto python-mox3 python-pil python-ply libssl-dev zlib1g-dev libbz2-dev libexpat1-dev libbluetooth-dev libgdbm-dev dpkg-dev quilt autotools-dev libreadline-dev libtinfo-dev libncursesw5-dev tk-dev blt-dev libssl-dev zlib1g-dev libbz2-dev libexpat1-dev libbluetooth-dev libsqlite3-dev libgpm2 mime-support netbase net-tools bzip2 python-virtualenv
cd /tmp
wget https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tgz
tar xvf Python-2.7.11.tgz
cd Python-2.7.11
./configure --prefix /usr/local/lib/python2.7.11
sudo make
sudo make install
cd /home/vagrant/
virtualenv --python=/usr/local/lib/python2.7.11/bin/python ri_dnsdb_client-python_2.7.11
source /home/vagrant/ri_dnsdb_client-python_2.7.11/bin/activate
pip install https://github.com/renisac/pdnssdk-py/archive/main.tar.gz
echo "source /home/vagrant/ri_dnsdb_client-python_2.7.11/bin/activate" >> /home/vagrant/.bashrc
echo "export PDNS_REMOTE=https://pdns.ren-isac.net" >> /home/vagrant/.bashrc
SCRIPT

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = 'ubuntu/trusty64'
  config.vm.provision "shell", inline: $script

  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--cpus", "2", "--ioapic", "on", "--memory", "512" ]
  end

  if File.file?(VAGRANTFILE_LOCAL)
    external = File.read VAGRANTFILE_LOCAL
    eval external
  end
end
