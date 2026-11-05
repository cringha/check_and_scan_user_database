import ecdsa
import hashlib

# 1. 生成密钥对（使用 secp256k1 曲线，比特币同款）
private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
public_key = private_key.get_verifying_key()

print(private_key.to_pem())
print(public_key.to_pem())

# 2. 待签名的消息
message = b"Hello, ECC!"

# 3. 签名（自动使用 SHA-256 哈希）
signature = private_key.sign(message, hashfunc=hashlib.sha256)

# 4. 验证签名
try:
    assert public_key.verify(signature, message, hashfunc=hashlib.sha256)
    print("✅ 签名验证通过")
except AssertionError:
    print("❌ 签名验证失败")

# 5. 篡改消息后验证（应失败）
tampered = b"Hello, hacker!"
try:
    assert public_key.verify(signature, tampered, hashfunc=hashlib.sha256)
    print("❌ 篡改后竟然通过了（不应该发生）")
except AssertionError:
    print("✅ 篡改消息后验证失败，符合预期")
