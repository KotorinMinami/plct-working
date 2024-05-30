# Sail 关于 hex_str 函数的不安全 bug 分析

## Bug 详情

在引用sail的hex_str时，在将str字符串转为对应的数值时，sail缺失了对于传入参数的检查，导致可能出现传入的字符串对应数值溢出的情况。

## hex_str 原理库分析

在sail中，我们在将对应的数值转换为十六进制字符串时一般使用的格式如：

```
let foo：string = hex_bits_8(0x0F)
```

而对应的函数 `hex_bits_n()` 实际上是库函数 `hex_bits()` 的包装，其定义一个双射，将数值与字符串相映射，其签名中的n对应的就是传入参数中的数值长度 `n` ：

```
mapping hex_bits_1 : bits(1) <-> string = { hex_bits(1, s) <-> s }
mapping hex_bits_2 : bits(2) <-> string = { hex_bits(2, s) <-> s }
mapping hex_bits_3 : bits(3) <-> string = { hex_bits(3, s) <-> s }
...
mapping hex_bits_31 : bits(31) <-> string = { hex_bits(31, s) <-> s }
mapping hex_bits_32 : bits(32) <-> string = { hex_bits(32, s) <-> s }
```

而函数 `hex_bits()` 对应另一个双射，其将数值与元组进行映射,其中元组包含数值长度以及字符串，其签名如下：

```
val hex_bits : forall 'n, 'n > 0. bits('n) <-> (int('n), string)
```

而此函数的具体实现需要较多的逻辑，由于为双射，故包括forwards与backwards部分，其中forwards函数将数值转为对应信息的元组，由于其将对应二进制串以unsigned处理为无符号数值，且转变为某个无符号数值后其总能转为对应的十六进制字符串，其并没有什么问题，故检查合法性的函数被赋值为true，不进行检查：

```
function hex_bits_forwards(bv) = (length(bv), hex_str(unsigned(bv)))
function hex_bits_forwards_matches(bv) = true
```

另一方面，backwards函数将元组转为对应的数值，其将对应的十六进制字符串转为对应的二进制串，由于其将对应的十六进制字符串一位位转变回对应数值，而指定的str存在非法值（即存在非十六进制字符串的情况），故其并不能够保证对应的数值能够被二进制串表示，故检查合法性的函数被赋值为库函数 `valid_hex_bits`，需要检查：

```
function hex_bits_backwards(n, str) = parse_hex_bits(n, str)
function hex_bits_backwards_matches(n, str) = valid_hex_bits(n, str)
```
## Bug分析

而上述bug的原因，追根溯源就出现在库函数 `valid_hex_bits` 以及 `parse_hex_bits` 中，其C语言后端如下：

```
void parse_hex_bits(lbits *res, const mpz_t n, const_sail_string hex)
{
  if (strncmp(hex, "0x", 2) != 0) {
    goto failure;
  }

  mpz_t value;
  mpz_init(value);
  if (mpz_set_str(value, hex + 2, 16) == 0) {
    res->len = mpz_get_ui(n);
    mpz_set(*res->bits, value);
    mpz_clear(value);
    return;
  }
  mpz_clear(value);

  // On failure, we return a zero bitvector of the correct width
failure:
  res->len = mpz_get_ui(n);
  mpz_set_ui(*res->bits, 0);
}

bool valid_hex_bits(const mpz_t n, const_sail_string hex) {
  if (strncmp(hex, "0x", 2) != 0) {
    return false;
  }

  for (int i = 2; i < strlen(hex); i++) {
    char c = hex[i];
    if (!((c >= '0' && c <= '9') || (c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F'))) {
      return false;
    }
  }

  return true;
}
```
其中可看到 `valid_hex_bits` 函数只对字符串`hex`是否为十六进制字符串进行检查，而并没有对`hex`是否与其对应的n数值长度相匹配进行检查，故其可能出现溢出的情况。如`valid_hex_bits(3, "0xF")` 在此逻辑中为真。

## Bug修复

而修复此bug，只需要在 `valid_hex_bits` 函数中添加对`hex`是否与其对应的n数值长度相匹配的检查，同时使得 `parse_hex_bits` 函数受 `valid_hex_bits`的检验即可(已修复)。

## 目前影响

目前此bug对sail model的运行是没有影响的，因为实际上sail model在执行elf文件时，只是以elf的阅读方式读入对应的编码，然后使用`bits -> ast`的映射定位到对应的指令的ast, 执行ast对应的执行函数后，在将对应的指令转为string 打印到log 中，而对应的另一方面的映射可以说目前没有使用到，只有在使用sail将对应的项目里信息输出为JSON 时才体现出来，这也是目前来说sail上游并没有察觉到此函数存在问题的原因。但即使如此，也不能改变其实际上是一个逻辑上的bug的事实，此修改依然避免了之后可能产生的其他问题，同时也使sail模拟器运行更为严谨。
