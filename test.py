#TODO: Make this into a true unit test implementation.
import IncludeSwitch
import hashlib

IncludeSwitch.modify_codebase_includes(".", IncludeSwitch.EXTENSIONS)



with open("test_ref.gls_") as f:
    contents = f.read().strip()
    test_ref_gls_hash_digest = hashlib.md5(contents).digest()

with open(IncludeSwitch.TEMP_GLS_NAME) as f:
    contents = f.read().strip()
    temp_gls_hash_digest = hashlib.md5(contents).digest()

with open("test_ref.h_") as f:
    contents = f.read().strip()
    test_ref_h_hash_digest = hashlib.md5(contents).digest()

with open(IncludeSwitch.TEMP_HEADER_NAME) as f:
    contents = f.read().strip()
    temp_h_hash_digest = hashlib.md5(contents).digest()

print "TESTING..."
print "GLS COMPARE TEST:",  "PASS" if test_ref_gls_hash_digest == temp_gls_hash_digest else "FAIL"
print "HEADER COMPARE TEST:",  "PASS" if test_ref_h_hash_digest == temp_h_hash_digest else "FAIL"
