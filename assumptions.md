# Assumptions

## General

- There is exactly one query per line
- All words are case insensitive
- Multiple names may refer to the same number
- A number-word may be reassigned to a different letter, overwriting the old letter
- Numbers and materials are a single word each
- There may be multiple currencies
- Different currencies do not have a fixed exchange rate since they might assign different values to materials (e.g: 1 *gold* is worth 2 *shiny-rocks* or 5 *coins*; if *copper* is worth 4 *shiny-rocks* we can not infer the price of *copper* in *coins*)
- The price of a material may be updated by specifying the new exchange rate
- In the statement *[material] is [number] [currency]* the material count is omitted and is therefore assumed to be 1
- In the query *how many [currency] is [material] ?* the count is omitted and is therefore assumed to be 1


## Input formatting

The input complies with the following extended Backus-Naur form

```
<input>             = ( <line> )*
<line>              = "#" <comment>
                    | [ "> " ] <query>
<comment>           = ( "#" | <letter> | <digit> | " " )+
<query>             = <number-definition>
                    | <price-definition>
                    | <number-question>
                    | <price-question>
<number-definition> = <word> " is " <numeral>
<price-definition>  = <count> <word> "is" <number> <word>
<number-question>   = "how much is " <count> " ?"
<price-question>    = "how many " <word> " is " <count> <word> " ?"

<word>              = ( <letter> )+
<letter>            = "A" | "B" | ... | "Z" | "a" | "b" | ... | "z"
<count>             = ( <word> )*
<numeral>           = "I" | "V" | "X" | "L" | "C" | "D" | "M"
<number>            = ( <digit> )+
<digit>             = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```

Using this syntax we can distinguish the 4 types of `query` lines easily.
Only `questions` end with the symbol `?`; `number-question` and `price-question` can be distinguished by their start: *how much* vs *how many*. On the other hand `number definitions` contain exactly 3 words whereas `price definitions` contain at least 4 words.
