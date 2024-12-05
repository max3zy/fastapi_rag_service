import hashlib


class Hasher:
    """
    выбор метода хэширования
    """
    _hasher: object

    @staticmethod
    def __xxhash64(value: str) -> str:
        import xxhash

        return str(xxhash.xxh64_intdigest(value))

    @staticmethod
    def __hashlib_sha512(value: str):
        return hashlib.sha512(value.encode()).hexdigest()

    # @staticmethod
    # def __metrohash64int(value: str) -> str:
    #     import metrohash
    #     return str(metrohash.hash64_int(value))

    def __init__(self, hasher: str) -> None:
        if hasher:
            if hasher in ("pyhash_metro64", "pyhash_xxhash64"):
                import pyhash

                self._hasher = (
                    pyhash.metro_64() if "pyhash_metro64" else pyhash.xx_64()
                )
            elif hasher == "xxhash64":
                self._hasher = self.__xxhash64
            elif hasher == "hashlib_sha512":
                self._hasher = self.__hashlib_sha512
            # elif hasher == "metrohash64":
            #     self._hasher = self.__metrohash64int
        else:
            raise ImportError("Please fill param settings.POSTGRES_HASHER")

    def hash_data(self, data: str) -> str:
        return self._hasher(data)
