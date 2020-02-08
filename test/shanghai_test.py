#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import unittest

# Add the repo root to the Python module path.
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src import shanghai
from src.shanghai import ArithmeticExpr
from src.shanghai import LiteralExpr
from src.shanghai import BasicTokenize
from src.shanghai import CallExpr
from src.shanghai import ComparisonExpr
from src.shanghai import ConcatExpr
from src.shanghai import IdentifierToken
from src.shanghai import IntegerLiteralExpr
from src.shanghai import Keyword
from src.shanghai import ParenExpr
from src.shanghai import ParseChars
from src.shanghai import ParseExprFromStr
from src.shanghai import ParseInteger
from src.shanghai import ParseStmtFromStr
from src.shanghai import ParseToAst
from src.shanghai import Run
from src.shanghai import STMT_ASSIGN
from src.shanghai import STMT_CALL
from src.shanghai import STMT_CONDITIONAL
from src.shanghai import STMT_DEC_BY
from src.shanghai import STMT_FUNC_DEF
from src.shanghai import STMT_INC_BY
from src.shanghai import STMT_LOOP
from src.shanghai import STMT_SAY
from src.shanghai import Statement
from src.shanghai import StringLiteralExpr
from src.shanghai import TK_CHAR
from src.shanghai import TK_IDENTIFIER
from src.shanghai import TK_INTEGER_LITERAL
from src.shanghai import TK_STRING_LITERAL
from src.shanghai import Token
from src.shanghai import Tokenize
from src.shanghai import VariableExpr

class shanghaiParseExprTest(unittest.TestCase):
  def testParseInteger(self):
    self.assertEqual(ParseExprFromStr('5')[0],
                     IntegerLiteralExpr(5))
    self.assertEqual(ParseExprFromStr('九')[0],
                     IntegerLiteralExpr(9))

  def testParseStringLiteral(self):
    self.assertEqual(ParseExprFromStr('“ 哈  哈   ”')[0],
                     StringLiteralExpr(' 哈  哈   '))

  def testParseIdentifier(self):
    self.assertEqual(ParseExprFromStr('阿庆')[0],
                     VariableExpr('阿庆'))

  def testParseParens(self):
    # Wide parens.
    self.assertEqual(ParseExprFromStr('（阿庆）')[0],
                     ParenExpr(
                         VariableExpr('阿庆')))
    # Narrow parens.
    self.assertEqual(ParseExprFromStr('(阿庆)')[0],
                     ParenExpr(
                         VariableExpr('阿庆')))

  def testParseCallExpr(self):
    self.assertEqual(ParseExprFromStr('白相阿庆')[0],
                     CallExpr('阿庆', []))
    self.assertEqual(ParseExprFromStr('白相阿庆（5）')[0],
                     CallExpr('阿庆',
                              [IntegerLiteralExpr(5)]))
    self.assertEqual(ParseExprFromStr('白相阿庆(6)')[0],
                     CallExpr('阿庆',
                              [IntegerLiteralExpr(6)]))
    self.assertEqual(ParseExprFromStr('白相阿庆(阿德，6)')[0],
                     CallExpr('阿庆',
                              [VariableExpr('阿德'),
                               IntegerLiteralExpr(6)]))
    self.assertEqual(ParseExprFromStr('白相阿庆(“你”，阿德，6)')[0],
                     CallExpr('阿庆',
                              [StringLiteralExpr('你'),
                               VariableExpr('阿德'),
                               IntegerLiteralExpr(6)]))
    self.assertEqual(ParseExprFromStr('白相阿庆(“你”,阿德，6)')[0],
                     CallExpr('阿庆',
                              [StringLiteralExpr('你'),
                               VariableExpr('阿德'),
                               IntegerLiteralExpr(6)]))

  def testParseTermExpr(self):
    self.assertEqual(ParseExprFromStr('阿庆乘五')[0],
                     ArithmeticExpr(
                         VariableExpr('阿庆'),
                         Keyword('乘'),
                         IntegerLiteralExpr(5))
                     )
    self.assertEqual(ParseExprFromStr('五除以阿庆')[0],
                     ArithmeticExpr(
                         IntegerLiteralExpr(5),
                         Keyword('除以'),
                         VariableExpr('阿庆'))
                     )
    self.assertEqual(ParseExprFromStr('五除以阿庆乘阿德')[0],
                     ArithmeticExpr(
                         ArithmeticExpr(
                             IntegerLiteralExpr(5),
                             Keyword('除以'),
                             VariableExpr('阿庆')),
                         Keyword('乘'),
                         VariableExpr('阿德')
                     ))

  def testParseArithmeticExpr(self):
    self.assertEqual(ParseExprFromStr('5加六')[0],
                     ArithmeticExpr(
                         IntegerLiteralExpr(5),
                         Keyword('加'),
                         IntegerLiteralExpr(6)
                     ))
    self.assertEqual(ParseExprFromStr('5加六乘3')[0],
                     ArithmeticExpr(
                         IntegerLiteralExpr(5),
                         Keyword('加'),
                         ArithmeticExpr(
                             IntegerLiteralExpr(6),
                             Keyword('乘'),
                             IntegerLiteralExpr(3))))
    self.assertEqual(ParseExprFromStr('5减六减阿庆')[0],
                     ArithmeticExpr(
                         ArithmeticExpr(
                             IntegerLiteralExpr(5),
                             Keyword('减'),
                             IntegerLiteralExpr(6)
                         ),
                         Keyword('减'),
                         VariableExpr('阿庆'))
                     )

  def testParseComparisonExpr(self):
    self.assertEqual(ParseExprFromStr('5比6老卵')[0],
                     ComparisonExpr(
                         IntegerLiteralExpr(5),
                         Keyword('老卵'),
                         IntegerLiteralExpr(6)
                     ))
    self.assertEqual(ParseExprFromStr('阿庆加5比6推板')[0],
                     ComparisonExpr(
                         ArithmeticExpr(
                             VariableExpr('阿庆'),
                             Keyword('加'),
                             IntegerLiteralExpr(5)),
                         Keyword('推板'),
                         IntegerLiteralExpr(6)
                     ))
    self.assertEqual(ParseExprFromStr('阿庆帮阿德一色一样')[0],
                     ComparisonExpr(
                         VariableExpr('阿庆'),
                         Keyword('一色一样'),
                         VariableExpr('阿德')
                     ))
    self.assertEqual(ParseExprFromStr('阿庆加5帮6伐大一样')[0],
                     ComparisonExpr(
                         ArithmeticExpr(
                             VariableExpr('阿庆'),
                             Keyword('加'),
                             IntegerLiteralExpr(5)),
                         Keyword('伐大一样'),
                         IntegerLiteralExpr(6)
                     ))

  def testParseConcatExpr(self):
    self.assertEqual(ParseExprFromStr('阿庆、2')[0],
                     ConcatExpr([
                         VariableExpr('阿庆'),
                         IntegerLiteralExpr(2)
                     ]))
  def testParseConcatExpr(self):
    self.assertEqual(ParseExprFromStr('阿庆加油、2、“哈”')[0],
                     ConcatExpr([
                         ArithmeticExpr(
                             VariableExpr('阿庆'),
                             Keyword('加'),
                             VariableExpr('油')),
                         IntegerLiteralExpr(2),
                         StringLiteralExpr('哈')
                     ]))

class shanghaiParseStatementTest(unittest.TestCase):
  def testParseConditional(self):
    self.assertEqual(
        ParseStmtFromStr('轧苗头：阿庆比五老卵？要来赛就嘎讪胡：阿庆。')[0],
        Statement(STMT_CONDITIONAL,
                  (ComparisonExpr(
                      VariableExpr('阿庆'),
                      Keyword('老卵'),
                      IntegerLiteralExpr(5)),
                   # then-branch
                   Statement(STMT_SAY,
                             VariableExpr('阿庆')),
                   # else-branch
                   None
                  )))

class shanghaiTest(unittest.TestCase):
  def testRunEmptyProgram(self):
    self.assertEqual(Run(''), '')

  def testRunHelloWorld(self):
    self.assertEqual(
        Run('嘎讪胡：“申花老卵！”。'),
        '申花老卵！\n')

  def testRunHelloWorld2(self):
    self.assertEqual(
        Run('嘎讪胡：“上港老卵！”。'),
        '上港老卵！\n')

  def testVarDecl(self):
    self.assertEqual(
        Run('阿德是则赤佬。'), '')

  def testVarAssignment(self):
    self.assertEqual(
        Run('阿德是则赤佬。\n阿德毛估估是250。\n嘎讪胡：阿德。'), '250\n')

  def testTokenize(self):
    self.assertEqual(
        list(BasicTokenize('【阶乘】')),
        [IdentifierToken('阶乘'),])
    self.assertEqual(
        list(BasicTokenize('【 阶  乘   】')),
        [IdentifierToken('阶乘'),])
    self.assertEqual(
        list(BasicTokenize('【阶乘】（那啥）')),
        [IdentifierToken('阶乘'),
         Keyword('（'),
         Token(TK_CHAR, '那'),
         Token(TK_CHAR, '啥'),
         Keyword('）'),])
    self.assertEqual(
        list(BasicTokenize('“ ”')),
        [Keyword('“'),
         Token(TK_STRING_LITERAL, ' '),
         Keyword('”'),])
    self.assertEqual(
        list(BasicTokenize('“”')),
        [Keyword('“'),
         Token(TK_STRING_LITERAL, ''),
         Keyword('”'),])
    self.assertEqual(
        list(BasicTokenize('“ A B ”')),
        [Keyword('“'),
         Token(TK_STRING_LITERAL, ' A B '),
         Keyword('”'),])
    self.assertEqual(
        list(BasicTokenize('阿德')),
        [Token(TK_CHAR, '阿'),
         Token(TK_CHAR, '德'),])
    self.assertEqual(
        list(BasicTokenize('  阿 德   ')),
        [Token(TK_CHAR, '阿'),
         Token(TK_CHAR, '德'),])
    self.assertEqual(
        list(Tokenize('# 123456\n阿德')),
        [IdentifierToken('阿德')])
    self.assertEqual(
        list(Tokenize('阿德')),
        [IdentifierToken('阿德')])
    self.assertEqual(
        ParseInteger('阿德'),
        (None, '阿德'))
    self.assertEqual(
        list(ParseChars('阿德')),
        [IdentifierToken('阿德')])
    self.assertEqual(
        list(Tokenize('阿德是则赤佬')),
        [IdentifierToken('阿德'),
         Keyword('是则赤佬')])
    self.assertEqual(
        list(Tokenize('阿德是 则\n赤佬 。 ')),
        [IdentifierToken('阿德'),
         Keyword('是则赤佬'),
         Keyword('。'),
        ])
    self.assertEqual(
        list(Tokenize('阿德是则赤佬。\n阿庆是则赤佬。\n')),
        [IdentifierToken('阿德'),
         Keyword('是则赤佬'),
         Keyword('。'),
         IdentifierToken('阿庆'),
         Keyword('是则赤佬'),
         Keyword('。'),
        ])
    self.assertEqual(
        list(Tokenize('阿德毛估估是250。\n阿庆毛估估是阿德。\n')),
        [IdentifierToken('阿德'),
         Keyword('毛估估是'),
         Token(TK_INTEGER_LITERAL, 250),
         Keyword('。'),
         IdentifierToken('阿庆'),
         Keyword('毛估估是'),
         IdentifierToken('阿德'),
         Keyword('。')])
    self.assertEqual(
        list(Tokenize('嘎讪胡：“你好”。')),
        [Keyword('嘎讪胡'),
         Keyword('：'),
         Keyword('“'),
         Token(TK_STRING_LITERAL, '你好'),
         Keyword('”'),
         Keyword('。')])

  def testTokenizeArithmetic(self):
    self.assertEqual(
        list(Tokenize('250加13减二乘五除以九')),
        [Token(TK_INTEGER_LITERAL, 250),
         Keyword('加'),
         Token(TK_INTEGER_LITERAL, 13),
         Keyword('减'),
         Token(TK_INTEGER_LITERAL, 2),
         Keyword('乘'),
         Token(TK_INTEGER_LITERAL, 5),
         Keyword('除以'),
         Token(TK_INTEGER_LITERAL, 9),
        ])

  def testTokenizeLoop(self):
    self.assertEqual(
        list(Tokenize('阿庆从1到9搞七捻三：搞好了。')),
        [IdentifierToken('阿庆'),
         Keyword('从'),
         Token(TK_INTEGER_LITERAL, 1),
         Keyword('到'),
         Token(TK_INTEGER_LITERAL, 9),
         Keyword('搞七捻三：'),
         Keyword('搞好了'),
         Keyword('。'),
        ])

  def testTokenizeCompound(self):
    self.assertEqual(
        list(Tokenize('一道组特：\n  嘎讪胡：阿庆。\n组好了。')),
        [Keyword('一道组特：'),
         Keyword('嘎讪胡'),
         Keyword('：'),
         IdentifierToken('阿庆'),
         Keyword('。'),
         Keyword('组好了'),
         Keyword('。'),])

  def testTokenizingIncrements(self):
    self.assertEqual(
        list(Tokenize('阿庆扎台型')),
        [IdentifierToken('阿庆'),
         Keyword('扎台型'),])
    self.assertEqual(
        list(Tokenize('阿庆扎两趟')),
        [IdentifierToken('阿庆'),
         Keyword('扎'),
         Token(TK_INTEGER_LITERAL, 2),
         Keyword('趟'),
        ])

  def testTokenizingDecrements(self):
    self.assertEqual(
        list(Tokenize('阿庆混腔势')),
        [IdentifierToken('阿庆'),
         Keyword('混腔势'),])
    self.assertEqual(
        list(Tokenize('阿庆混三趟')),
        [IdentifierToken('阿庆'),
         Keyword('混'),
         Token(TK_INTEGER_LITERAL, 3),
         Keyword('趟'),
        ])

  def testTokenizingConcat(self):
    self.assertEqual(
        list(Tokenize('阿德、二')),
        [IdentifierToken('阿德'),
         Keyword('、'),
         Token(TK_INTEGER_LITERAL, 2),])

  def testTokenizingFuncDef(self):
    self.assertEqual(
        list(Tokenize('写九九表哪能组：组好了。')),
        [IdentifierToken('写九九表'),
         Keyword('哪能组：'),
         Keyword('组好了'),
         Keyword('。'),])

  def testTokenizingFuncCall(self):
    self.assertEqual(
        list(Tokenize('白相写九九表')),
        [Keyword('白相'),
         IdentifierToken('写九九表'),])

  def testParsingIncrements(self):
    self.assertEqual(
        ParseToAst('阿庆扎台型。'),
        [Statement(
            STMT_INC_BY,
            (IdentifierToken('阿庆'),
             IntegerLiteralExpr(1)))])
    self.assertEqual(
        ParseToAst('阿庆扎两趟。'),
        [Statement(
            STMT_INC_BY,
            (IdentifierToken('阿庆'),
             IntegerLiteralExpr(2)))])

  def testParsingDecrements(self):
    self.assertEqual(
        ParseToAst('阿庆混腔势。'),
        [Statement(
            STMT_DEC_BY,
            (IdentifierToken('阿庆'),
             IntegerLiteralExpr(1)))])
    self.assertEqual(
        ParseToAst('阿庆混三趟。'),
        [Statement(
            STMT_DEC_BY,
            (IdentifierToken('阿庆'),
             IntegerLiteralExpr(3)))])

  def testParsingLoop(self):
    self.assertEqual(
        ParseToAst('阿庆从1到9搞七捻三：搞好了。'),
        [Statement(
            STMT_LOOP,
            (IdentifierToken('阿庆'),
             IntegerLiteralExpr(1),
             IntegerLiteralExpr(9),
             []))])

  def testParsingComparison(self):
    self.assertEquals(
        ParseToAst('嘎讪胡：2比5老卵。'),
        [Statement(
            STMT_SAY,
            ComparisonExpr(IntegerLiteralExpr(2),
                           Keyword('老卵'),
                           IntegerLiteralExpr(5)
            ))])

  def testParsingFuncDef(self):
    self.assertEqual(
        ParseToAst('写九九表哪能组：组好了。'),
        [Statement(STMT_FUNC_DEF,
                   (IdentifierToken('写九九表'),
                    [],  # Formal parameters.
                    []  # Function body.
                   ))])
    self.assertEqual(
        ParseToAst('写九九表哪能组：嘎讪胡：1。组好了。'),
        [Statement(STMT_FUNC_DEF,
                   (IdentifierToken('写九九表'),
                    [],  # Formal parameters.
                    # Function body.
                    [Statement(STMT_SAY,
                               LiteralExpr(Token(
                                   TK_INTEGER_LITERAL, 1)))]
                   ))])

  def testParsingFuncDefWithParam(self):
    self.assertEqual(
        ParseToAst('【阶乘】（那啥）哪能组：组好了。'),
        [Statement(STMT_FUNC_DEF,
                   (IdentifierToken('阶乘'),
                    [IdentifierToken('那啥')],  # Formal parameters.
                    []  # Function body.
                   ))])

  def testParsingFuncCallWithParam(self):
    self.assertEqual(
        ParseToAst('白相【阶乘】（五）。'),
        [Statement(STMT_CALL,
                   CallExpr('阶乘',
                            [IntegerLiteralExpr(5)]))])

  def testVarAssignmentFromVar(self):
    self.assertEqual(
        Run('阿德是则赤佬。\n阿庆是则赤佬。\n'
                    '阿德毛估估是250。\n阿庆毛估估是阿德。\n嘎讪胡：阿庆。'), '250\n')

  def testIncrements(self):
    self.assertEqual(
        Run('阿德是则赤佬。阿德毛估估是二。阿德扎台型。嘎讪胡：阿德。'),
        '3\n')
    self.assertEqual(
        Run('阿德是则赤佬。阿德毛估估是三。阿德扎五趟。嘎讪胡：阿德。'),
        '8\n')

  def testDecrements(self):
    self.assertEqual(
        Run('阿德是则赤佬。阿德毛估估是二。阿德混腔势。嘎讪胡：阿德。'),
        '1\n')
    self.assertEqual(
        Run('阿德是则赤佬。阿德毛估估是三。阿德混五趟。嘎讪胡：阿德。'),
        '-2\n')

  def testLoop(self):
    self.assertEqual(
        Run('阿德从1到3搞七捻三：嘎讪胡：阿德。搞好了。'),
        '1\n2\n3\n')

  def testLoopWithNoStatement(self):
    self.assertEqual(
        Run('阿德从1到2搞七捻三：搞好了。'),
        '')

  def testLoopWithMultipleStatements(self):
    self.assertEqual(
        Run('阿德从1到2搞七捻三：嘎讪胡：阿德。嘎讪胡：阿德加一。搞好了。'),
        '1\n2\n2\n3\n')

  def testPrintBool(self):
    self.assertEqual(
        Run('阿庆是则赤佬。嘎讪胡：阿庆。嘎讪胡：阿庆脑子瓦特了。'),
        '脑子瓦特了\n对额\n')
    self.assertEqual(
        Run('嘎讪胡：五比二老卵。'),
        '对额\n')
    self.assertEqual(
        Run('嘎讪胡：五比二老卵、五比二推板、一帮2一色一样、1帮二伐大一样。'),
        '对额勿对勿对对额\n')

  def testDelete(self):
    self.assertEqual(
      Run('阿庆是则赤佬。阿庆毛估估是二。色特阿庆！嘎讪胡：阿庆。'),
      '脑子瓦特了\n')

  def testIntegerLiteral(self):
    self.assertEqual(
      Run('嘎讪胡：零。'),
      '0\n')
    self.assertEqual(
      Run('嘎讪胡：一。'),
      '1\n')
    self.assertEqual(
      Run('嘎讪胡：二。'),
      '2\n')
    self.assertEqual(
      Run('嘎讪胡：两。'),
      '2\n')
    self.assertEqual(
      Run('嘎讪胡：良。'),
      '2\n')
    self.assertEqual(
      Run('嘎讪胡：三。'),
      '3\n')
    self.assertEqual(
      Run('嘎讪胡：赛。'),
      '3\n')
    self.assertEqual(
      Run('嘎讪胡：四。'),
      '4\n')
    self.assertEqual(
      Run('嘎讪胡：五。'),
      '5\n')
    self.assertEqual(
      Run('嘎讪胡：六。'),
      '6\n')
    self.assertEqual(
      Run('嘎讪胡：七。'),
      '7\n')
    self.assertEqual(
      Run('嘎讪胡：八。'),
      '8\n')
    self.assertEqual(
      Run('嘎讪胡：九。'),
      '9\n')
    self.assertEqual(
      Run('嘎讪胡：十。'),
      '10\n')

  def testArithmetic(self):
    self.assertEqual(
      Run('嘎讪胡：五加二。'),
      '7\n')
    self.assertEqual(
      Run('嘎讪胡：五减二。'),
      '3\n')
    self.assertEqual(
      Run('嘎讪胡：五乘二。'),
      '10\n')
    self.assertEqual(
      Run('嘎讪胡：十除以二。'),
      '5.0\n')
    self.assertEqual(
      Run('嘎讪胡：十除以得毕挺三。'),
      '3\n')
    self.assertEqual(
      Run('嘎讪胡：五加七乘二。'),
      '19\n')
    self.assertEqual(
      Run('嘎讪胡：（五加七）乘二。'),
      '24\n')
    self.assertEqual(
      Run('嘎讪胡：(五加七)乘二。'),
      '24\n')
    self.assertEqual(
      Run('嘎讪胡：(五减（四减三）)乘二。'),
      '8\n')

  def testConcat(self):
    self.assertEqual(
        Run('嘎讪胡：“牛”、二。'),
        '牛2\n')
    self.assertEqual(
        Run('嘎讪胡：“阿庆”、665加一。'),
        '阿庆666\n')

  def testCompound(self):
    self.assertEqual(
        Run('一道组特：组好了。'),
        '')
    self.assertEqual(
        Run('一道组特：嘎讪胡：1。组好了。'),
        '1\n')
    self.assertEqual(
        Run('一道组特：嘎讪胡：1。嘎讪胡：2。组好了。'),
        '1\n2\n')

  def testRunConditional(self):
    self.assertEqual(
        Run('轧苗头：5比2老卵？要来赛就嘎讪胡：“OK”。'),
        'OK\n')
    self.assertEqual(
        Run('轧苗头：5比2老卵？要来赛就一道组特：\n'
            '组好了。'),
        '')
    self.assertEqual(
        Run('轧苗头：5比2老卵？\n'
            '要来赛就一道组特：\n'
            '    嘎讪胡：5。\n'
            '组好了。'),
        '5\n')
    self.assertEqual(
        Run('轧苗头：5比6老卵？要来赛就嘎讪胡：“OK”。\n'
            '勿来赛就嘎讪胡：“不OK”。'),
        '不OK\n')
    self.assertEqual(
        Run('轧苗头：5比6老卵？\n'
            '要来赛就嘎讪胡：“OK”。\n'
            '勿来赛就一道组特：\n'
            '  嘎讪胡：“不OK”。\n'
            '  嘎讪胡：“还是不OK”。\n'
            '组好了。'),
        '不OK\n还是不OK\n')
    # Else should match the last If.
    self.assertEqual(
        Run('''
          轧苗头：2比1老卵？   # condition 1: True
          要来赛就轧苗头：2比3老卵？  # condition 2: False
              要来赛就嘎讪胡：“A”。  # for condition 2
              勿来赛就嘎讪胡：“B”。# for condition 2
          '''),
        'B\n')

  def testRunFunc(self):
    self.assertEqual(
        Run('埋汰哪能组：嘎讪胡：“侬是小瘪三”。组好了。'),
        '')
    self.assertEqual(
        Run('埋汰哪能组：嘎讪胡：“侬是小瘪三”。组好了。白相埋汰。'),
        '侬是小瘪三\n')

  def testFuncCallWithParam(self):
    self.assertEqual(
        Run('【加一】（那啥）哪能组：嘎讪胡：那啥加一。组好了。\n'
                    '白相【加一】（五）。'),
        '6\n')

  def testFuncWithReturnValue(self):
    self.assertEqual(
        Run('【加一】（那啥）哪能组：再会那啥加一。组好了。\n'
                    '嘎讪胡：白相【加一】（二）。'),
        '3\n')

  def testRecursiveFunc(self):
    self.assertEqual(
        Run('''
【阶乘】（那啥）哪能组：
轧苗头：那啥比一推板？
要来赛就再会一。
再会那啥乘白相【阶乘】（那啥减一）。
组好了。

嘎讪胡：白相【阶乘】（五）。
        '''),
        '120\n')

  def testMultiArgFunc(self):
    self.assertEqual(
        Run('''
求和（甲，乙）哪能组：
  再会 甲加乙。
组好了。

嘎讪胡：白相求和（五，七）。
        '''),
        '12\n')
    self.assertEqual(
        Run('''
求和（甲，乙）哪能组：
  嘎讪胡：甲加乙。
组好了。

白相求和（五，七）。
        '''),
        '12\n')

  def testNormalizingBang(self):
    self.assertEqual(
        Run('【加一】（那啥）哪能组：嘎讪胡：那啥加一！组好了！\n'
                    '白相【加一】（五）！'),
        '6\n')

  def testImport(self):
    self.assertEqual(
      Run('''
      阿庆，上 re。
      轧苗头：白相re.match（“a.*”，“abc”）？
      要来赛就嘎讪胡：“OK”。
      '''),
      'OK\n')

if __name__ == '__main__':
  unittest.main()
