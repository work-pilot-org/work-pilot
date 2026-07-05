from src.core.security import hash_password, verify_password


class TestHashPassword:
    def test_returns_a_string(self):
        hashed = hash_password("Sup3rSecret!")

        assert isinstance(hashed, str)

    def test_hash_is_not_equal_to_plain_password(self):
        password = "Sup3rSecret!"

        assert hash_password(password) != password

    def test_hash_uses_a_bcrypt_identifier_prefix(self):
        hashed = hash_password("Sup3rSecret!")

        assert hashed.startswith(("$2a$", "$2b$", "$2y$"))

    def test_hashing_the_same_password_twice_produces_different_hashes(self):
        # bcrypt salts each hash, so two hashes of the same password must
        # never be equal.
        password = "Sup3rSecret!"

        assert hash_password(password) != hash_password(password)

    def test_supports_unicode_passwords(self):
        hashed = hash_password("p\u00e4ssw\u00f6rd\u2122")

        assert isinstance(hashed, str)

    def test_long_password_beyond_bcrypt_72_byte_limit_does_not_raise(self):
        # bcrypt truncates input at 72 bytes; this is the exact scenario the
        # bcrypt==4.0.1 pin (see pyproject.toml) protects against, since
        # newer bcrypt releases raise instead of truncating.
        long_password = "a" * 100

        hashed = hash_password(long_password)

        assert isinstance(hashed, str)


class TestVerifyPassword:
    def test_correct_password_verifies_true(self):
        password = "Sup3rSecret!"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_incorrect_password_verifies_false(self):
        hashed = hash_password("Sup3rSecret!")

        assert verify_password("WrongPassword!", hashed) is False

    def test_empty_password_does_not_verify_against_a_real_hash(self):
        hashed = hash_password("Sup3rSecret!")

        assert verify_password("", hashed) is False

    def test_verification_is_case_sensitive(self):
        hashed = hash_password("CaseSensitive")

        assert verify_password("casesensitive", hashed) is False