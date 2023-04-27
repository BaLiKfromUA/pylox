import pytest

from pylox.error import LoxSyntaxError
from pylox.scanner import Scanner
from pylox.tokens import TokenType


def test_if_identifiers_scanning_is_valid() -> None:
    # GIVEN
    src = "andy formless fo _ _123 _abc ab123 abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"
    expected_token_lexemes = src.split(" ")

    # WHEN
    tokens = Scanner(src).scan_tokens()

    # THEN
    assert len(tokens) == 9
    assert tokens[-1].token_type == TokenType.EOF

    for ind in range(8):
        assert tokens[ind].token_type == TokenType.IDENTIFIER
        assert tokens[ind].lexeme == expected_token_lexemes[ind]


def test_if_keyword_scanning_is_valid() -> None:
    # GIVEN
    src = "and class else false for fun if nil or return super this true var while"
    expected_token_lexemes = src.split(" ")

    # WHEN
    tokens = Scanner(src).scan_tokens()

    # THEN
    assert len(tokens) == 16
    assert tokens[-1].token_type == TokenType.EOF

    for ind in range(15):
        assert (
            str(tokens[ind].token_type)
            == f"TokenType.{expected_token_lexemes[ind].upper()}"
        )
        assert tokens[ind].lexeme == expected_token_lexemes[ind]


def test_if_numbers_scanning_is_valid() -> None:
    # GIVEN
    src = """
    123
    123.456
    .456
    123.
    
    // expect: NUMBER 123 123.0
    // expect: NUMBER 123.456 123.456
    // expect: DOT . null
    // expect: NUMBER 456 456.0
    // expect: NUMBER 123 123.0
    // expect: DOT . null
    // expect: EOF  null
    """

    # WHEN
    tokens = Scanner(src).scan_tokens()

    # THEN
    assert len(tokens) == 7
    assert tokens[-1].token_type == TokenType.EOF

    assert tokens[2].token_type == tokens[5].token_type == TokenType.DOT

    assert tokens[0].token_type == tokens[4].token_type == TokenType.NUMBER
    assert tokens[0].literal == tokens[4].literal == 123

    assert tokens[1].token_type == TokenType.NUMBER
    assert tokens[1].lexeme == "123.456"
    assert tokens[1].literal == 123.456


# todo: test escape sequences
def test_if_strings_scanning_is_valid() -> None:
    # GIVEN
    src = """
    ""
    "string"

    // expect: STRING "" 
    // expect: STRING "string" string
    // expect: EOF  null
    """

    # WHEN
    tokens = Scanner(src).scan_tokens()

    # THEN
    assert len(tokens) == 3
    assert tokens[-1].token_type == TokenType.EOF

    assert tokens[0].token_type == tokens[1].token_type == TokenType.STRING
    assert tokens[0].literal == ""
    assert tokens[1].literal == "string"


def test_if_punctuators_scanning_is_valid() -> None:
    # GIVEN
    src = "(){};,+-*!===<=>=!=<>/."
    expected_token_types = [
        TokenType.LEFT_PAREN,
        TokenType.RIGHT_PAREN,
        TokenType.LEFT_BRACE,
        TokenType.RIGHT_BRACE,
        TokenType.SEMICOLON,
        TokenType.COMMA,
        TokenType.PLUS,
        TokenType.MINUS,
        TokenType.STAR,
        TokenType.BANG_EQUAL,
        TokenType.EQUAL_EQUAL,
        TokenType.LESS_EQUAL,
        TokenType.GREATER_EQUAL,
        TokenType.BANG_EQUAL,
        TokenType.LESS,
        TokenType.GREATER,
        TokenType.SLASH,
        TokenType.DOT,
        TokenType.EOF,
    ]

    # WHEN
    tokens = Scanner(src).scan_tokens()

    # THEN
    assert len(tokens) == len(expected_token_types)

    for i in range(len(tokens)):
        assert tokens[i].token_type == expected_token_types[i]


def test_if_whitespace_is_ignored() -> None:
    # GIVEN
    src = """
    space    tabs				newlines




    end

    // expect: IDENTIFIER space null
    // expect: IDENTIFIER tabs null
    // expect: IDENTIFIER newlines null
    // expect: IDENTIFIER end null
    // expect: EOF  null
    """

    # WHEN
    tokens = Scanner(src).scan_tokens()

    # THEN
    assert len(tokens) == 5
    assert tokens[-1].token_type == TokenType.EOF

    for i in range(4):
        assert tokens[i].token_type == TokenType.IDENTIFIER


def test_if_multiline_comments_works() -> None:
    # GIVEN
    src = """
    /* simple one line */ // test simple comment
    "hello"
    /* /* nesting */ */
    
    /* */ /* /* /* */ */ */
    "world"
    
    // hey
    """
    # WHEN
    tokens = Scanner(src).scan_tokens()

    # THEN
    assert len(tokens) == 3
    assert tokens[-1].token_type == TokenType.EOF
    assert tokens[0].token_type == tokens[1].token_type == TokenType.STRING

    assert tokens[0].literal == "hello"
    assert tokens[1].literal == "world"


def test_if_unterminated_string_produces_error() -> None:
    src = '"hello" "world!'

    with pytest.raises(LoxSyntaxError):
        Scanner(src).scan_tokens()


def test_if_unknown_symbol_produces_error() -> None:
    src = "%"

    with pytest.raises(LoxSyntaxError):
        Scanner(src).scan_tokens()


def test_if_unclosed_multiline_comment_produces_error() -> None:
    src = "/* /* */ //"

    with pytest.raises(LoxSyntaxError):
        Scanner(src).scan_tokens()
