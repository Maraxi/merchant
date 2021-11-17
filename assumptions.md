# Assumptions

## General

- All words are case insensitive
- Different numbers have different names
- Multiple names may refer to the same number
- Numbers and materials are a single word each
- There may be multiple currencies
- Different currencies do not have a fixed exchange rate since they might assign different values to materials (e.g: 1 *gold* is worth 2 *shiny-rocks* or 5 *coins*; if *copper* is worth 4 *shiny-rocks* we can not infer the price of *copper* in *coins*)
- The price of a material may be updated by specifying the new exchange rate


## Input formating

The input complies with the following extended Backus-Naur form

```
<input>             = ( <line> )*
<line>              = "#" <comment>
                    | [ "> " ] <query>
<comment>           = ( "#" | <letter> | <digit> | " " )+
<query>             = <number-definition>
                    | <price-definition>
                    | <question>
<number-definition> = <word> " is " <numeral>
<price-definition>  = <count> <word> "is" <number> <word>
<question>          = "how many " <word> " is " <count> <word> " ?"

<word>              = ( <letter> )+
<letter>            = "A" | "B" | ... | "Z" | "a" | "b" | ... | "z"
<count>             = ( <word> )+
<numeral>           = "I" | "V" | "X" | "L" | "C" | "D" | "M"
<number>            = ( <digit> )+
<digit>             = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```

Using this syntax we can distinguish the 3 types of `query` lines easily.
Only `question`s end with the symbol `?`; All other querys contain either exactly 3 `word`s if they are a `number defintion` or more words if they are a `price-definition`.
