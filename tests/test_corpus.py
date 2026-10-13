import pytest

from src.corpus import list_corpus_profiles, load_corpus, load_the_prince_corpus
from src.chunking import build_chunks
from src.retrieval import retrieve_top_k
from src.rag import build_grounded_answer


def test_list_corpus_profiles_contains_expected_profiles() -> None:
    profiles = list_corpus_profiles()
    assert "default" in profiles
    assert "training-rag" in profiles
    assert "the-prince" in profiles


def test_load_training_rag_corpus_has_expected_topic() -> None:
    docs = load_corpus("training-rag")
    joined = " ".join(doc.text for doc in docs).lower()
    assert "citation" in joined
    assert "judge" in joined


def test_unknown_profile_raises() -> None:
    with pytest.raises(ValueError):
        load_corpus("unknown-profile")

def test_the_prince_corpus_loads() -> None:
    documents = load_the_prince_corpus()

    assert len(documents) == 1
    assert documents[0].doc_id == "book-1232"
    assert len(documents[0].text) > 1000

def test_the_prince_retrieves_principalities_content() -> None:
    documents = load_the_prince_corpus()
    chunks = build_chunks(documents, chunk_size=500, overlap=100)

    results = retrieve_top_k(
        "What kinds of principalities are there?",
        chunks,
        k=3,
    )

    assert results
    assert "princip" in results[0].chunk.text.lower()

def test_the_prince_refuses_unrelated_question() -> None:
    documents = load_the_prince_corpus()
    chunks = build_chunks(documents, chunk_size=500, overlap=100)

    result = build_grounded_answer(
        "What is the recipe for pizza in Belgrade?",
        chunks,
        top_k=3,
    )

    assert result.refused is True
    assert result.citations == []
