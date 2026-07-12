# endcord-textreplace
An extension for [endcord](https://github.com/sparklost/endcord) discord TUI client, that replaces message text with extended regex before its sent.

## Installing
See [official extensions documentation](https://github.com/sparklost/endcord/blob/main/docs/extensions.md#installing-extensions) for installing instructions.
Available options:
- Git clone into `Extensions` directory located in endcord config directory.
- Run `endcord -i https://github.com/sparklost/endcord-textreplace`
- Or use endcord client-side command `install_extension sparklost/endcord-textreplace`  

## Configuration
Replacement rules can be configured in `textreplace_rules.json` which is generated in endcord config dir.  
The rules are written in following format:
```json
[
  {
    "find": "text to be replaced in the message",
    "replace": "replacement",
    "includes": "replace if message includes this, this key is optional"
  },
  {
    "find_re": "\\*(f|F|c|C)",
    "replace:": "°$1"
  }
]
```
**IMPORTANT: backslashes must be escaped!**  
Like in the example above, normal regex would be `\*(f|F|c|C)` but in json backslash must be escaped with another one: `\\*(f|F|c|C)`.  
`$1`, `$2`... are groups from regex match. `$&` is entire matched string. `$<name>` is named group. These can be used only in replacement string.  
If you want to replace only normal text then use `"find"` key. If you want to replace using regex then use `"find_re"` key.  
Dont forget to put `,`, but it must not be present on the last item.  
Check log for errors to see if json is correct, and what line and column in json is causing error.  
You can also verify json on online json checkers.


## Disclaimer
> [!WARNING]
> Using third-party client is against Discord's Terms of Service and may cause your account to be banned!  
> **Use endcord and/or this extension at your own risk!**  
> If this extension is modified, it may be used for harmful or unintended purposes.  
> **The developer is not responsible for any misuse or for actions taken by users.**  
