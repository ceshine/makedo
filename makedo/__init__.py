import poseidon as po

class AutoDO:
    def __init__(self):
        # The key should be stored in DIGITALOCEAN_API_KEY environment variable
        self._client = po.client.connect() 

    def _snapshot(self, droplet, snapshot_name):
        droplet.power_off() # snapshots are only allowed while powered off
        # TODO: check if the snapshot name already exists?
        droplet.take_snapshot(snapshot_name)
        print "Creating snapshot..."
        if snapshot_name in [x['name'] for x in droplet.snapshots()]:
            return True
        else:
            raise RuntimeError("Snapshot failed.")

    def destroy(self, droplet_name):
        droplet = self._client.droplets.by_name(droplet_name)
        return droplet.delete()
        
    def snapshot_and_destroy(self, droplet_name, snapshot_name):
        # Raise KeyError if can't find a droplet by name
        droplet = self._client.droplets.by_name(droplet_name)
        self._snapshot(droplet, snapshot_name)
        return droplet.delete()

    def find_snapshot(self, snapshot_name):
        # https://developers.digitalocean.com/#retrieve-an-existing-image-by-slug
        # Doesn't get implemented in poseidon
        for snapshot in self.list_snapshots():
            if snapshot['name'] == snapshot_name:
                return snapshot['id']
        
    def create_droplete_from_snapshot(self, droplet_name, region,
                                      snapshot_name, ssh_keys=None, size="512mb"):
        image = self.find_snapshot(snapshot_name)
        if ssh_keys is not None:
            keys = []
            for name in ssh_keys:
                key = self.find_ssh_key(name)
                if key is None:
                    raise NameError("Cannot find ssh key named " + name)
                keys.append(key['id'])
            ssh_keys = keys
        return self._client.droplets.create(droplet_name, region, size,
                                     image, ssh_keys=ssh_keys)

    def list_ssh_keys(self):
        return self._client.keys.list()

    def find_ssh_key(self, name):
        for key in self.list_ssh_keys():
            if key['name'] == name:
                return key
        return None

    def list_snapshots(self):
        images = self._client.images.list()
        snapshots = []
        for image in images:
            if not image['public']:
                snapshots.append(image)
        return snapshots

    def list_sizes(self):
        return self._client.sizes.list()
