import pickle

from datasets import load_dataset
from plaid.containers.sample import Sample

hf_dataset = load_dataset("PLAID-datasets/VKI-LS59", split="all_samples")

ids_train = hf_dataset.description["split"]["train"]
ids_test = hf_dataset.description["split"]["test"]

sample_train_0 = Sample.model_validate(pickle.loads(hf_dataset[ids_train[0]]["sample"]))

tree = sample_train_0.get_mesh()

from Muscat.Bridges import CGNSBridge, PyVistaBridge

muscat_mesh = CGNSBridge.CGNSToMesh(tree, baseNames=["Base_2_2"])
print(muscat_mesh)
pv_mesh = PyVistaBridge.MeshToPyVista(muscat_mesh)

pv_mesh["mach"] = muscat_mesh.nodeFields["mach"]
pv_mesh.plot(cpos="xy", cmap="mach")

# print(pv_mesh)
