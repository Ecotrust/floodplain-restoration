Vagrant::Config.run do |config|
  config.vm.define "stage" do |stage|
    stage.vm.box = "trusty64_custom"
    # created with 
    #    vagrant package --base precise64-custom2
    stage.vm.box_url = "http://labs.ecotrust.org/vagrant_boxes/trusty64_custom.box"
    
    stage.vm.customize [
            'modifyvm', :id,
            "--memory", 868,
            "--cpus", 2]

    # ssh defaults to 2222
    stage.vm.forward_port 80, 8089
    stage.vm.forward_port 8009, 8009
    
    # In this case, we don't share the folder
    # Treat this machine like a staging environment and deploy with git via ansible
    # exactly as we would in production
    # stage.vm.share_folder "v-app", "/usr/local/apps/floodplain-restoration", "./", owner:"www-data"

    # provisioning not handled by vagrant; done directly with ansible, see deploy/*.sh
  end
end
