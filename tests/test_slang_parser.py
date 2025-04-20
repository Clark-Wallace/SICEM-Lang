import pytest
from slang_parser import SlangParser

def test_simple_function_parsing():
    content = """
    system: TestSystem

    function: greet
    agent: GreeterAI
    intent: say hello
    input: name
    output: greeting
    """
    parser = SlangParser()
    parsed = parser.parse(content)
    assert parsed['system']['name'] == 'TestSystem'
    funcs = parsed['functions']
    assert len(funcs) == 1
    fn = funcs[0]
    assert fn['name'] == 'greet'
    assert fn['agent'] == 'GreeterAI'
    assert fn['intent'] == 'say hello'
    assert fn['input'] == 'name'
    assert fn['output'] == 'greeting'

def test_function_with_context():
    content = """
    system: CtxtSys

    function: analyze
    agent: Analyzer
    intent: process data
    context:
      data_type: text
      complexity: high
    input: text_data
    output: analysis_result
    """
    parser = SlangParser()
    parsed = parser.parse(content)
    fn = parsed['functions'][0]
    assert fn['context']['data_type'] == 'text'
    assert fn['context']['complexity'] == 'high'

def test_no_functions():
    content = "system: EmptySys"
    parser = SlangParser()
    parsed = parser.parse(content)
    assert parsed['system']['name'] == 'EmptySys'
    assert parsed['functions'] == []