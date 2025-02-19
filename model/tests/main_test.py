import pytest
from fastapi.testclient import TestClient
from model.main import app, setup_model


# --- Dummy Classes for Mocking spaCy and scispaCy Behavior --- #


class DummyEntity:
    def __init__(self, text, label, umls_ents):
        self.text = text
        self.label_ = label
        # Create a dummy namespace for custom attributes.
        self._ = type("DummyExtension", (), {})()
        self._.umls_ents = umls_ents


class DummyDoc:
    def __init__(self, ents):
        self.ents = ents


class DummyLinker:
    def __init__(self, cui_to_entity):
        # Simulate a simple UMLS mapping.
        self.umls = type("DummyUMLS", (), {})()
        self.umls.cui_to_entity = cui_to_entity


class DummyNLP:
    def __init__(self):
        # Initialize a dummy linker with one entity detail.
        self.linker = DummyLinker(
            {
                "C0000870": type(
                    "EntityDetail",
                    (),
                    {"canonical_name": "Ibuprofen", "aliases": ["Advil", "Motrin", "Brufen"]},
                )()
            }
        )

    def __call__(self, text):
        # Simulate the extraction of a single entity.
        dummy_entity = DummyEntity("advil", "CHEMICAL", [("C0000870", 0.95)])
        return DummyDoc([dummy_entity])

    def get_pipe(self, name):
        if name == "scispacy_linker":
            return self.linker
        raise ValueError("Pipe not found")


# --- Pytest Fixtures and Tests --- #


@pytest.fixture
def client():
    # Override the dependency to return the dummy NLP model.
    app.dependency_overrides[setup_model] = lambda: DummyNLP()
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()


def test_health(http_client):
    response = http_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "Service is healthy" in data["message"]


def test_process_text(http_client):
    payload = {"text": "The patient took advil."}
    response = http_client.post("/extract_entities", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "entities" in data
    entities = data["entities"]
    assert len(entities) == 1

    entity = entities[0]
    assert entity["text"] == "advil"
    assert entity["label"] == "CHEMICAL"

    umls_entities = entity["umls_entities"]
    assert len(umls_entities) == 1

    umls_entity = umls_entities[0]
    assert umls_entity["cui"] == "C0000870"
    assert umls_entity["score"] == 0.95
    assert umls_entity["canonical_name"] == "Ibuprofen"
    assert "Advil" in umls_entity["aliases"]
