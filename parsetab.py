
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'T_APACHE_LOCATION_DIRECTIVE T_COMMENT T_CONFIG_DIRECTIVE T_CONFIG_DIRECTIVE_ARGUMENT_NOTQUOTE T_CONFIG_DIRECTIVE_ARGUMENT_QUOTE_DOUBLE T_CONFIG_DIRECTIVE_ARGUMENT_QUOTE_SINGLE T_CONFIG_DIRECTIVE_SECACTION T_CONFIG_DIRECTIVE_SECRULE T_EXCLUSION_MARK T_INCLUDE_DIRECTIVE T_INCLUDE_DIRECTIVE_ARGUMENT T_INCLUDE_DIRECTIVE_ARGUMENT_QUOTED T_SECRULE_ACTION T_SECRULE_ACTION_ARGUMENT T_SECRULE_ACTION_ARGUMENT_QUOTE_SINGLE T_SECRULE_ACTION_ARGUMENT_VALUE T_SECRULE_ACTION_ARGUMENT_VALUE_PARAMETER T_SECRULE_ACTION_ARGUMENT_VALUE_PARAMETER_ARGUMENT T_SECRULE_ACTION_ARGUMENT_VALUE_PARAMETER_COLON T_SECRULE_ACTION_COLON T_SECRULE_ACTION_EQUALMARK T_SECRULE_ACTION_QUOTE_MARK T_SECRULE_ACTION_SEMICOLON T_SECRULE_ACTION_SEPARATOR T_SECRULE_OPERATOR T_SECRULE_OPERATOR_ARGUMENT T_SECRULE_OPERATOR_QUOTE_MARK T_SECRULE_OPERATOR_WITH_EXCLAMMARK T_SECRULE_VARIABLE T_SECRULE_VARIABLE_COUNTER T_SECRULE_VARIABLE_PART T_SECRULE_VARIABLE_PART_QUOTED T_SECRULE_VARIABLE_PART_QUOTED_REGEX T_SECRULE_VARIABLE_SEPARATORmodsec_config : comment_line\n                         | modsec_config comment_line\n                         | include_line\n                         | modsec_config include_line\n                         | directive_line\n                         | modsec_config directive_line\n                         | secaction_line\n                         | modsec_config secaction_line\n                         | secrule_line\n                         | modsec_config secrule_linecomment_line : T_COMMENTinclude_line : include_line_unquoted_argument\n                        | include_line_quoted_argumentinclude_line_unquoted_argument : T_INCLUDE_DIRECTIVE T_INCLUDE_DIRECTIVE_ARGUMENTinclude_line_quoted_argument : T_INCLUDE_DIRECTIVE T_INCLUDE_DIRECTIVE_ARGUMENT_QUOTEDdirective_line : tok_directive\n                          | tok_directive tok_directive_argument_list\n                          | tok_directive_apache_locationtok_directive : T_CONFIG_DIRECTIVEtok_directive_argument_list : tok_directive_argument\n                                       | tok_directive_argument_list tok_directive_argumenttok_directive_argument : tok_directive_argument_notquoted\n                                  | tok_directive_argument_quoted_double\n                                  | tok_directive_argument_quoted_singletok_directive_argument_notquoted : T_CONFIG_DIRECTIVE_ARGUMENT_NOTQUOTEtok_directive_argument_quoted_double : T_CONFIG_DIRECTIVE_ARGUMENT_QUOTE_DOUBLEtok_directive_argument_quoted_single : T_CONFIG_DIRECTIVE_ARGUMENT_QUOTE_SINGLEtok_directive_apache_location : T_APACHE_LOCATION_DIRECTIVEsecaction_line : tok_confdir_secaction T_SECRULE_ACTION_QUOTE_MARK secaction_expr_list T_SECRULE_ACTION_QUOTE_MARKtok_confdir_secaction : T_CONFIG_DIRECTIVE_SECACTIONsecrule_line : secrule_directive secrule_argument_list secrule_operator_expression secrule_actions\n                        | secrule_directive secrule_argument_list secrule_operator_expressionsecrule_directive : T_CONFIG_DIRECTIVE_SECRULEsecrule_argument_list : secrule_variable_listsecrule_variable_list : secrule_variable\n                                 | secrule_variable_exclusion\n                                 | secrule_variable_counter\n                                 | secrule_variable_with_part\n                                 | secrule_variable_exclusion_with_part\n                                 | secrule_variable_list secrule_variable_separator secrule_variable\n                                 | secrule_variable_list secrule_variable_separator secrule_variable_counter\n                                 | secrule_variable_list secrule_variable_separator secrule_variable_with_part\n                                 | secrule_variable_list secrule_variable_separator secrule_variable_exclusion\n                                 | secrule_variable_list secrule_variable_separator secrule_variable_exclusion_with_partsecrule_variable : T_SECRULE_VARIABLEsecrule_variable_exclusion : T_EXCLUSION_MARK  T_SECRULE_VARIABLEsecrule_variable_with_part : T_SECRULE_VARIABLE T_SECRULE_VARIABLE_PART\n                                      | T_SECRULE_VARIABLE T_SECRULE_VARIABLE_PART_QUOTED\n                                      | T_SECRULE_VARIABLE T_SECRULE_VARIABLE_PART_QUOTED_REGEXsecrule_variable_exclusion_with_part : T_EXCLUSION_MARK T_SECRULE_VARIABLE T_SECRULE_VARIABLE_PART\n                                                | T_EXCLUSION_MARK T_SECRULE_VARIABLE T_SECRULE_VARIABLE_PART_QUOTED\n                                                | T_EXCLUSION_MARK T_SECRULE_VARIABLE T_SECRULE_VARIABLE_PART_QUOTED_REGEXsecrule_variable_counter : secrule_variable_counter_only\n                                    | secrule_variable_counter_with_varsecrule_variable_counter_only : T_SECRULE_VARIABLE_COUNTER T_SECRULE_VARIABLEsecrule_variable_counter_with_var : T_SECRULE_VARIABLE_COUNTER T_SECRULE_VARIABLE T_SECRULE_VARIABLE_PART\n                                             | T_SECRULE_VARIABLE_COUNTER T_SECRULE_VARIABLE T_SECRULE_VARIABLE_PART_QUOTED\n                                             | T_SECRULE_VARIABLE_COUNTER T_SECRULE_VARIABLE T_SECRULE_VARIABLE_PART_QUOTED_REGEXsecrule_variable_separator : T_SECRULE_VARIABLE_SEPARATORsecrule_operator_expression : secrule_operator_expression_quoted\n                                       | secrule_operator_or_argument\n                                       | secrule_operator_and_argumentsecrule_operator_expression_quoted : T_SECRULE_OPERATOR_QUOTE_MARK secrule_operator_or_argument T_SECRULE_OPERATOR_QUOTE_MARK\n                                              | T_SECRULE_OPERATOR_QUOTE_MARK secrule_operator_and_argument T_SECRULE_OPERATOR_QUOTE_MARKsecrule_operator_or_argument : secrule_operator_only\n                                        | secrule_operator_argument_onlysecrule_operator_only : T_SECRULE_OPERATOR\n                                 | T_SECRULE_OPERATOR_WITH_EXCLAMMARKsecrule_operator_argument_only : T_SECRULE_OPERATOR_ARGUMENTsecrule_operator_and_argument : T_SECRULE_OPERATOR T_SECRULE_OPERATOR_ARGUMENT\n                                         | T_SECRULE_OPERATOR_WITH_EXCLAMMARK T_SECRULE_OPERATOR_ARGUMENTsecrule_actions : T_SECRULE_ACTION_QUOTE_MARK secrule_actions_list T_SECRULE_ACTION_QUOTE_MARK\n                           | secrule_actions_listsecrule_actions_list : secaction_expr\n                                | secaction_expr_list secaction_exprsecaction_expr_list  : secaction_expr\n                                | secaction_expr_list secaction_exprsecaction_expr : secaction_single\n                          | secaction_with_argument\n                          | secaction_with_quoted_argument\n                          | secaction_with_argument_with_value\n                          | secaction_with_argument_with_value_and_param\n                          | secaction_with_argument_with_value_and_param_paramarg\n                          | T_SECRULE_ACTION_SEPARATORsecaction_single : T_SECRULE_ACTIONsecaction_with_argument : T_SECRULE_ACTION T_SECRULE_ACTION_COLON T_SECRULE_ACTION_ARGUMENTsecaction_with_quoted_argument : T_SECRULE_ACTION T_SECRULE_ACTION_COLON T_SECRULE_ACTION_ARGUMENT_QUOTE_SINGLE T_SECRULE_ACTION_ARGUMENT T_SECRULE_ACTION_ARGUMENT_QUOTE_SINGLEsecaction_with_argument_with_value : T_SECRULE_ACTION T_SECRULE_ACTION_COLON T_SECRULE_ACTION_ARGUMENT T_SECRULE_ACTION_EQUALMARK T_SECRULE_ACTION_ARGUMENT_VALUEsecaction_with_argument_with_value_and_param : T_SECRULE_ACTION T_SECRULE_ACTION_COLON T_SECRULE_ACTION_ARGUMENT T_SECRULE_ACTION_EQUALMARK T_SECRULE_ACTION_ARGUMENT_VALUE T_SECRULE_ACTION_SEMICOLON T_SECRULE_ACTION_ARGUMENT_VALUE_PARAMETERsecaction_with_argument_with_value_and_param_paramarg : T_SECRULE_ACTION T_SECRULE_ACTION_COLON T_SECRULE_ACTION_ARGUMENT T_SECRULE_ACTION_EQUALMARK T_SECRULE_ACTION_ARGUMENT_VALUE T_SECRULE_ACTION_SEMICOLON T_SECRULE_ACTION_ARGUMENT_VALUE_PARAMETER T_SECRULE_ACTION_ARGUMENT_VALUE_PARAMETER_COLON T_SECRULE_ACTION_ARGUMENT_VALUE_PARAMETER_ARGUMENT'
    
_lr_action_items = {'T_COMMENT':([0,1,2,3,4,5,6,7,8,9,10,11,15,16,19,20,21,22,23,24,25,26,27,28,29,30,31,45,46,47,50,51,52,53,54,55,56,57,58,59,60,61,63,64,65,66,67,75,78,80,81,85,86,98,101,102,103,106,107,108,110,112,],[7,7,-1,-3,-5,-7,-9,-11,-12,-13,-16,-18,-19,-28,-2,-4,-6,-8,-10,-17,-20,-22,-23,-24,-25,-26,-27,-14,-15,-21,-78,-79,-80,-81,-82,-83,-84,-85,-32,-60,-61,-62,-65,-66,-67,-69,-68,-29,-31,-73,-74,-70,-71,-86,-75,-63,-64,-72,-88,-87,-89,-90,]),'T_INCLUDE_DIRECTIVE':([0,1,2,3,4,5,6,7,8,9,10,11,15,16,19,20,21,22,23,24,25,26,27,28,29,30,31,45,46,47,50,51,52,53,54,55,56,57,58,59,60,61,63,64,65,66,67,75,78,80,81,85,86,98,101,102,103,106,107,108,110,112,],[14,14,-1,-3,-5,-7,-9,-11,-12,-13,-16,-18,-19,-28,-2,-4,-6,-8,-10,-17,-20,-22,-23,-24,-25,-26,-27,-14,-15,-21,-78,-79,-80,-81,-82,-83,-84,-85,-32,-60,-61,-62,-65,-66,-67,-69,-68,-29,-31,-73,-74,-70,-71,-86,-75,-63,-64,-72,-88,-87,-89,-90,]),'T_CONFIG_DIRECTIVE':([0,1,2,3,4,5,6,7,8,9,10,11,15,16,19,20,21,22,23,24,25,26,27,28,29,30,31,45,46,47,50,51,52,53,54,55,56,57,58,59,60,61,63,64,65,66,67,75,78,80,81,85,86,98,101,102,103,106,107,108,110,112,],[15,15,-1,-3,-5,-7,-9,-11,-12,-13,-16,-18,-19,-28,-2,-4,-6,-8,-10,-17,-20,-22,-23,-24,-25,-26,-27,-14,-15,-21,-78,-79,-80,-81,-82,-83,-84,-85,-32,-60,-61,-62,-65,-66,-67,-69,-68,-29,-31,-73,-74,-70,-71,-86,-75,-63,-64,-72,-88,-87,-89,-90,]),'T_APACHE_LOCATION_DIRECTIVE':([0,1,2,3,4,5,6,7,8,9,10,11,15,16,19,20,21,22,23,24,25,26,27,28,29,30,31,45,46,47,50,51,52,53,54,55,56,57,58,59,60,61,63,64,65,66,67,75,78,80,81,85,86,98,101,102,103,106,107,108,110,112,],[16,16,-1,-3,-5,-7,-9,-11,-12,-13,-16,-18,-19,-28,-2,-4,-6,-8,-10,-17,-20,-22,-23,-24,-25,-26,-27,-14,-15,-21,-78,-79,-80,-81,-82,-83,-84,-85,-32,-60,-61,-62,-65,-66,-67,-69,-68,-29,-31,-73,-74,-70,-71,-86,-75,-63,-64,-72,-88,-87,-89,-90,]),'T_CONFIG_DIRECTIVE_SECACTION':([0,1,2,3,4,5,6,7,8,9,10,11,15,16,19,20,21,22,23,24,25,26,27,28,29,30,31,45,46,47,50,51,52,53,54,55,56,57,58,59,60,61,63,64,65,66,67,75,78,80,81,85,86,98,101,102,103,106,107,108,110,112,],[17,17,-1,-3,-5,-7,-9,-11,-12,-13,-16,-18,-19,-28,-2,-4,-6,-8,-10,-17,-20,-22,-23,-24,-25,-26,-27,-14,-15,-21,-78,-79,-80,-81,-82,-83,-84,-85,-32,-60,-61,-62,-65,-66,-67,-69,-68,-29,-31,-73,-74,-70,-71,-86,-75,-63,-64,-72,-88,-87,-89,-90,]),'T_CONFIG_DIRECTIVE_SECRULE':([0,1,2,3,4,5,6,7,8,9,10,11,15,16,19,20,21,22,23,24,25,26,27,28,29,30,31,45,46,47,50,51,52,53,54,55,56,57,58,59,60,61,63,64,65,66,67,75,78,80,81,85,86,98,101,102,103,106,107,108,110,112,],[18,18,-1,-3,-5,-7,-9,-11,-12,-13,-16,-18,-19,-28,-2,-4,-6,-8,-10,-17,-20,-22,-23,-24,-25,-26,-27,-14,-15,-21,-78,-79,-80,-81,-82,-83,-84,-85,-32,-60,-61,-62,-65,-66,-67,-69,-68,-29,-31,-73,-74,-70,-71,-86,-75,-63,-64,-72,-88,-87,-89,-90,]),'$end':([1,2,3,4,5,6,7,8,9,10,11,15,16,19,20,21,22,23,24,25,26,27,28,29,30,31,45,46,47,50,51,52,53,54,55,56,57,58,59,60,61,63,64,65,66,67,75,78,80,81,85,86,98,101,102,103,106,107,108,110,112,],[0,-1,-3,-5,-7,-9,-11,-12,-13,-16,-18,-19,-28,-2,-4,-6,-8,-10,-17,-20,-22,-23,-24,-25,-26,-27,-14,-15,-21,-78,-79,-80,-81,-82,-83,-84,-85,-32,-60,-61,-62,-65,-66,-67,-69,-68,-29,-31,-73,-74,-70,-71,-86,-75,-63,-64,-72,-88,-87,-89,-90,]),'T_CONFIG_DIRECTIVE_ARGUMENT_NOTQUOTE':([10,15,24,25,26,27,28,29,30,31,47,],[29,-19,29,-20,-22,-23,-24,-25,-26,-27,-21,]),'T_CONFIG_DIRECTIVE_ARGUMENT_QUOTE_DOUBLE':([10,15,24,25,26,27,28,29,30,31,47,],[30,-19,30,-20,-22,-23,-24,-25,-26,-27,-21,]),'T_CONFIG_DIRECTIVE_ARGUMENT_QUOTE_SINGLE':([10,15,24,25,26,27,28,29,30,31,47,],[31,-19,31,-20,-22,-23,-24,-25,-26,-27,-21,]),'T_SECRULE_ACTION_QUOTE_MARK':([12,17,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,64,65,66,67,76,81,85,86,98,100,101,102,103,107,108,110,112,],[32,-30,75,-76,-78,-79,-80,-81,-82,-83,-84,-85,79,-60,-61,-62,-65,-66,-67,-69,-68,-77,-74,-70,-71,-86,106,-75,-63,-64,-88,-87,-89,-90,]),'T_SECRULE_VARIABLE':([13,18,41,44,68,69,],[40,-33,73,74,40,-59,]),'T_EXCLUSION_MARK':([13,18,68,69,],[41,-33,41,-59,]),'T_SECRULE_VARIABLE_COUNTER':([13,18,68,69,],[44,-33,44,-59,]),'T_INCLUDE_DIRECTIVE_ARGUMENT':([14,],[45,]),'T_INCLUDE_DIRECTIVE_ARGUMENT_QUOTED':([14,],[46,]),'T_SECRULE_ACTION_SEPARATOR':([32,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,64,65,66,67,76,79,81,82,85,86,98,101,102,103,107,108,110,112,],[56,56,-76,-78,-79,-80,-81,-82,-83,-84,-85,56,-60,-61,-62,-65,-66,-67,-69,-68,-77,56,-76,56,-70,-71,-86,-77,-63,-64,-88,-87,-89,-90,]),'T_SECRULE_ACTION':([32,48,49,50,51,52,53,54,55,56,57,58,59,60,61,63,64,65,66,67,76,79,81,82,85,86,98,101,102,103,107,108,110,112,],[57,57,-76,-78,-79,-80,-81,-82,-83,-84,-85,57,-60,-61,-62,-65,-66,-67,-69,-68,-77,57,-76,57,-70,-71,-86,-77,-63,-64,-88,-87,-89,-90,]),'T_SECRULE_OPERATOR_QUOTE_MARK':([33,34,35,36,37,38,39,40,42,43,63,64,65,66,67,70,71,72,73,74,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,],[62,-34,-35,-36,-37,-38,-39,-45,-53,-54,-65,-66,-67,-69,-68,-47,-48,-49,-46,-55,102,103,-70,-71,-40,-41,-42,-43,-44,-50,-51,-52,-56,-57,-58,]),'T_SECRULE_OPERATOR':([33,34,35,36,37,38,39,40,42,43,62,70,71,72,73,74,87,88,89,90,91,92,93,94,95,96,97,],[65,-34,-35,-36,-37,-38,-39,-45,-53,-54,65,-47,-48,-49,-46,-55,-40,-41,-42,-43,-44,-50,-51,-52,-56,-57,-58,]),'T_SECRULE_OPERATOR_WITH_EXCLAMMARK':([33,34,35,36,37,38,39,40,42,43,62,70,71,72,73,74,87,88,89,90,91,92,93,94,95,96,97,],[67,-34,-35,-36,-37,-38,-39,-45,-53,-54,67,-47,-48,-49,-46,-55,-40,-41,-42,-43,-44,-50,-51,-52,-56,-57,-58,]),'T_SECRULE_OPERATOR_ARGUMENT':([33,34,35,36,37,38,39,40,42,43,62,65,67,70,71,72,73,74,87,88,89,90,91,92,93,94,95,96,97,],[66,-34,-35,-36,-37,-38,-39,-45,-53,-54,66,85,86,-47,-48,-49,-46,-55,-40,-41,-42,-43,-44,-50,-51,-52,-56,-57,-58,]),'T_SECRULE_VARIABLE_SEPARATOR':([34,35,36,37,38,39,40,42,43,70,71,72,73,74,87,88,89,90,91,92,93,94,95,96,97,],[69,-35,-36,-37,-38,-39,-45,-53,-54,-47,-48,-49,-46,-55,-40,-41,-42,-43,-44,-50,-51,-52,-56,-57,-58,]),'T_SECRULE_VARIABLE_PART':([40,73,74,],[70,92,95,]),'T_SECRULE_VARIABLE_PART_QUOTED':([40,73,74,],[71,93,96,]),'T_SECRULE_VARIABLE_PART_QUOTED_REGEX':([40,73,74,],[72,94,97,]),'T_SECRULE_ACTION_COLON':([57,],[77,]),'T_SECRULE_ACTION_ARGUMENT':([77,99,],[98,105,]),'T_SECRULE_ACTION_ARGUMENT_QUOTE_SINGLE':([77,105,],[99,108,]),'T_SECRULE_ACTION_EQUALMARK':([98,],[104,]),'T_SECRULE_ACTION_ARGUMENT_VALUE':([104,],[107,]),'T_SECRULE_ACTION_SEMICOLON':([107,],[109,]),'T_SECRULE_ACTION_ARGUMENT_VALUE_PARAMETER':([109,],[110,]),'T_SECRULE_ACTION_ARGUMENT_VALUE_PARAMETER_COLON':([110,],[111,]),'T_SECRULE_ACTION_ARGUMENT_VALUE_PARAMETER_ARGUMENT':([111,],[112,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'modsec_config':([0,],[1,]),'comment_line':([0,1,],[2,19,]),'include_line':([0,1,],[3,20,]),'directive_line':([0,1,],[4,21,]),'secaction_line':([0,1,],[5,22,]),'secrule_line':([0,1,],[6,23,]),'include_line_unquoted_argument':([0,1,],[8,8,]),'include_line_quoted_argument':([0,1,],[9,9,]),'tok_directive':([0,1,],[10,10,]),'tok_directive_apache_location':([0,1,],[11,11,]),'tok_confdir_secaction':([0,1,],[12,12,]),'secrule_directive':([0,1,],[13,13,]),'tok_directive_argument_list':([10,],[24,]),'tok_directive_argument':([10,24,],[25,47,]),'tok_directive_argument_notquoted':([10,24,],[26,26,]),'tok_directive_argument_quoted_double':([10,24,],[27,27,]),'tok_directive_argument_quoted_single':([10,24,],[28,28,]),'secrule_argument_list':([13,],[33,]),'secrule_variable_list':([13,],[34,]),'secrule_variable':([13,68,],[35,87,]),'secrule_variable_exclusion':([13,68,],[36,90,]),'secrule_variable_counter':([13,68,],[37,88,]),'secrule_variable_with_part':([13,68,],[38,89,]),'secrule_variable_exclusion_with_part':([13,68,],[39,91,]),'secrule_variable_counter_only':([13,68,],[42,42,]),'secrule_variable_counter_with_var':([13,68,],[43,43,]),'secaction_expr_list':([32,58,79,],[48,82,82,]),'secaction_expr':([32,48,58,79,82,],[49,76,81,81,101,]),'secaction_single':([32,48,58,79,82,],[50,50,50,50,50,]),'secaction_with_argument':([32,48,58,79,82,],[51,51,51,51,51,]),'secaction_with_quoted_argument':([32,48,58,79,82,],[52,52,52,52,52,]),'secaction_with_argument_with_value':([32,48,58,79,82,],[53,53,53,53,53,]),'secaction_with_argument_with_value_and_param':([32,48,58,79,82,],[54,54,54,54,54,]),'secaction_with_argument_with_value_and_param_paramarg':([32,48,58,79,82,],[55,55,55,55,55,]),'secrule_operator_expression':([33,],[58,]),'secrule_operator_expression_quoted':([33,],[59,]),'secrule_operator_or_argument':([33,62,],[60,83,]),'secrule_operator_and_argument':([33,62,],[61,84,]),'secrule_operator_only':([33,62,],[63,63,]),'secrule_operator_argument_only':([33,62,],[64,64,]),'secrule_variable_separator':([34,],[68,]),'secrule_actions':([58,],[78,]),'secrule_actions_list':([58,79,],[80,100,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> modsec_config","S'",1,None,None,None),
  ('modsec_config -> comment_line','modsec_config',1,'p_config_line','msc_pyparser.py',763),
  ('modsec_config -> modsec_config comment_line','modsec_config',2,'p_config_line','msc_pyparser.py',764),
  ('modsec_config -> include_line','modsec_config',1,'p_config_line','msc_pyparser.py',765),
  ('modsec_config -> modsec_config include_line','modsec_config',2,'p_config_line','msc_pyparser.py',766),
  ('modsec_config -> directive_line','modsec_config',1,'p_config_line','msc_pyparser.py',767),
  ('modsec_config -> modsec_config directive_line','modsec_config',2,'p_config_line','msc_pyparser.py',768),
  ('modsec_config -> secaction_line','modsec_config',1,'p_config_line','msc_pyparser.py',769),
  ('modsec_config -> modsec_config secaction_line','modsec_config',2,'p_config_line','msc_pyparser.py',770),
  ('modsec_config -> secrule_line','modsec_config',1,'p_config_line','msc_pyparser.py',771),
  ('modsec_config -> modsec_config secrule_line','modsec_config',2,'p_config_line','msc_pyparser.py',772),
  ('comment_line -> T_COMMENT','comment_line',1,'p_comment_line','msc_pyparser.py',775),
  ('include_line -> include_line_unquoted_argument','include_line',1,'p_include_line','msc_pyparser.py',779),
  ('include_line -> include_line_quoted_argument','include_line',1,'p_include_line','msc_pyparser.py',780),
  ('include_line_unquoted_argument -> T_INCLUDE_DIRECTIVE T_INCLUDE_DIRECTIVE_ARGUMENT','include_line_unquoted_argument',2,'p_include_line_unquoted_argument','msc_pyparser.py',783),
  ('include_line_quoted_argument -> T_INCLUDE_DIRECTIVE T_INCLUDE_DIRECTIVE_ARGUMENT_QUOTED','include_line_quoted_argument',2,'p_include_line_quoted_argument','msc_pyparser.py',788),
  ('directive_line -> tok_directive','directive_line',1,'p_directive_line','msc_pyparser.py',793),
  ('directive_line -> tok_directive tok_directive_argument_list','directive_line',2,'p_directive_line','msc_pyparser.py',794),
  ('directive_line -> tok_directive_apache_location','directive_line',1,'p_directive_line','msc_pyparser.py',795),
  ('tok_directive -> T_CONFIG_DIRECTIVE','tok_directive',1,'p_tok_directive','msc_pyparser.py',799),
  ('tok_directive_argument_list -> tok_directive_argument','tok_directive_argument_list',1,'p_tok_directive_argument_list','msc_pyparser.py',803),
  ('tok_directive_argument_list -> tok_directive_argument_list tok_directive_argument','tok_directive_argument_list',2,'p_tok_directive_argument_list','msc_pyparser.py',804),
  ('tok_directive_argument -> tok_directive_argument_notquoted','tok_directive_argument',1,'p_tok_directive_argument','msc_pyparser.py',808),
  ('tok_directive_argument -> tok_directive_argument_quoted_double','tok_directive_argument',1,'p_tok_directive_argument','msc_pyparser.py',809),
  ('tok_directive_argument -> tok_directive_argument_quoted_single','tok_directive_argument',1,'p_tok_directive_argument','msc_pyparser.py',810),
  ('tok_directive_argument_notquoted -> T_CONFIG_DIRECTIVE_ARGUMENT_NOTQUOTE','tok_directive_argument_notquoted',1,'p_tok_directive_argument_notquoted','msc_pyparser.py',814),
  ('tok_directive_argument_quoted_double -> T_CONFIG_DIRECTIVE_ARGUMENT_QUOTE_DOUBLE','tok_directive_argument_quoted_double',1,'p_tok_directive_argument_quoted_double','msc_pyparser.py',818),
  ('tok_directive_argument_quoted_single -> T_CONFIG_DIRECTIVE_ARGUMENT_QUOTE_SINGLE','tok_directive_argument_quoted_single',1,'p_tok_directive_argument_quoted_single','msc_pyparser.py',822),
  ('tok_directive_apache_location -> T_APACHE_LOCATION_DIRECTIVE','tok_directive_apache_location',1,'p_tok_directive_apache_location','msc_pyparser.py',826),
  ('secaction_line -> tok_confdir_secaction T_SECRULE_ACTION_QUOTE_MARK secaction_expr_list T_SECRULE_ACTION_QUOTE_MARK','secaction_line',4,'p_secaction_line','msc_pyparser.py',830),
  ('tok_confdir_secaction -> T_CONFIG_DIRECTIVE_SECACTION','tok_confdir_secaction',1,'p_tok_confdir_secaction','msc_pyparser.py',835),
  ('secrule_line -> secrule_directive secrule_argument_list secrule_operator_expression secrule_actions','secrule_line',4,'p_secrule_line','msc_pyparser.py',840),
  ('secrule_line -> secrule_directive secrule_argument_list secrule_operator_expression','secrule_line',3,'p_secrule_line','msc_pyparser.py',841),
  ('secrule_directive -> T_CONFIG_DIRECTIVE_SECRULE','secrule_directive',1,'p_secrule_directive','msc_pyparser.py',846),
  ('secrule_argument_list -> secrule_variable_list','secrule_argument_list',1,'p_secrule_argument_list','msc_pyparser.py',851),
  ('secrule_variable_list -> secrule_variable','secrule_variable_list',1,'p_secrule_variable_list','msc_pyparser.py',855),
  ('secrule_variable_list -> secrule_variable_exclusion','secrule_variable_list',1,'p_secrule_variable_list','msc_pyparser.py',856),
  ('secrule_variable_list -> secrule_variable_counter','secrule_variable_list',1,'p_secrule_variable_list','msc_pyparser.py',857),
  ('secrule_variable_list -> secrule_variable_with_part','secrule_variable_list',1,'p_secrule_variable_list','msc_pyparser.py',858),
  ('secrule_variable_list -> secrule_variable_exclusion_with_part','secrule_variable_list',1,'p_secrule_variable_list','msc_pyparser.py',859),
  ('secrule_variable_list -> secrule_variable_list secrule_variable_separator secrule_variable','secrule_variable_list',3,'p_secrule_variable_list','msc_pyparser.py',860),
  ('secrule_variable_list -> secrule_variable_list secrule_variable_separator secrule_variable_counter','secrule_variable_list',3,'p_secrule_variable_list','msc_pyparser.py',861),
  ('secrule_variable_list -> secrule_variable_list secrule_variable_separator secrule_variable_with_part','secrule_variable_list',3,'p_secrule_variable_list','msc_pyparser.py',862),
  ('secrule_variable_list -> secrule_variable_list secrule_variable_separator secrule_variable_exclusion','secrule_variable_list',3,'p_secrule_variable_list','msc_pyparser.py',863),
  ('secrule_variable_list -> secrule_variable_list secrule_variable_separator secrule_variable_exclusion_with_part','secrule_variable_list',3,'p_secrule_variable_list','msc_pyparser.py',864),
  ('secrule_variable -> T_SECRULE_VARIABLE','secrule_variable',1,'p_secrule_variable','msc_pyparser.py',868),
  ('secrule_variable_exclusion -> T_EXCLUSION_MARK T_SECRULE_VARIABLE','secrule_variable_exclusion',2,'p_secrule_variable_exclusion','msc_pyparser.py',872),
  ('secrule_variable_with_part -> T_SECRULE_VARIABLE T_SECRULE_VARIABLE_PART','secrule_variable_with_part',2,'p_secrule_variable_with_part','msc_pyparser.py',876),
  ('secrule_variable_with_part -> T_SECRULE_VARIABLE T_SECRULE_VARIABLE_PART_QUOTED','secrule_variable_with_part',2,'p_secrule_variable_with_part','msc_pyparser.py',877),
  ('secrule_variable_with_part -> T_SECRULE_VARIABLE T_SECRULE_VARIABLE_PART_QUOTED_REGEX','secrule_variable_with_part',2,'p_secrule_variable_with_part','msc_pyparser.py',878),
  ('secrule_variable_exclusion_with_part -> T_EXCLUSION_MARK T_SECRULE_VARIABLE T_SECRULE_VARIABLE_PART','secrule_variable_exclusion_with_part',3,'p_secrule_variable_exclusion_with_part','msc_pyparser.py',887),
  ('secrule_variable_exclusion_with_part -> T_EXCLUSION_MARK T_SECRULE_VARIABLE T_SECRULE_VARIABLE_PART_QUOTED','secrule_variable_exclusion_with_part',3,'p_secrule_variable_exclusion_with_part','msc_pyparser.py',888),
  ('secrule_variable_exclusion_with_part -> T_EXCLUSION_MARK T_SECRULE_VARIABLE T_SECRULE_VARIABLE_PART_QUOTED_REGEX','secrule_variable_exclusion_with_part',3,'p_secrule_variable_exclusion_with_part','msc_pyparser.py',889),
  ('secrule_variable_counter -> secrule_variable_counter_only','secrule_variable_counter',1,'p_secrule_variable_counter','msc_pyparser.py',898),
  ('secrule_variable_counter -> secrule_variable_counter_with_var','secrule_variable_counter',1,'p_secrule_variable_counter','msc_pyparser.py',899),
  ('secrule_variable_counter_only -> T_SECRULE_VARIABLE_COUNTER T_SECRULE_VARIABLE','secrule_variable_counter_only',2,'p_secrule_variable_counter_only','msc_pyparser.py',903),
  ('secrule_variable_counter_with_var -> T_SECRULE_VARIABLE_COUNTER T_SECRULE_VARIABLE T_SECRULE_VARIABLE_PART','secrule_variable_counter_with_var',3,'p_secrule_variable_counter_with_var','msc_pyparser.py',907),
  ('secrule_variable_counter_with_var -> T_SECRULE_VARIABLE_COUNTER T_SECRULE_VARIABLE T_SECRULE_VARIABLE_PART_QUOTED','secrule_variable_counter_with_var',3,'p_secrule_variable_counter_with_var','msc_pyparser.py',908),
  ('secrule_variable_counter_with_var -> T_SECRULE_VARIABLE_COUNTER T_SECRULE_VARIABLE T_SECRULE_VARIABLE_PART_QUOTED_REGEX','secrule_variable_counter_with_var',3,'p_secrule_variable_counter_with_var','msc_pyparser.py',909),
  ('secrule_variable_separator -> T_SECRULE_VARIABLE_SEPARATOR','secrule_variable_separator',1,'p_secrule_variable_separator','msc_pyparser.py',921),
  ('secrule_operator_expression -> secrule_operator_expression_quoted','secrule_operator_expression',1,'p_secrule_operator_expression','msc_pyparser.py',925),
  ('secrule_operator_expression -> secrule_operator_or_argument','secrule_operator_expression',1,'p_secrule_operator_expression','msc_pyparser.py',926),
  ('secrule_operator_expression -> secrule_operator_and_argument','secrule_operator_expression',1,'p_secrule_operator_expression','msc_pyparser.py',927),
  ('secrule_operator_expression_quoted -> T_SECRULE_OPERATOR_QUOTE_MARK secrule_operator_or_argument T_SECRULE_OPERATOR_QUOTE_MARK','secrule_operator_expression_quoted',3,'p_secrule_operator_expression_quoted','msc_pyparser.py',931),
  ('secrule_operator_expression_quoted -> T_SECRULE_OPERATOR_QUOTE_MARK secrule_operator_and_argument T_SECRULE_OPERATOR_QUOTE_MARK','secrule_operator_expression_quoted',3,'p_secrule_operator_expression_quoted','msc_pyparser.py',932),
  ('secrule_operator_or_argument -> secrule_operator_only','secrule_operator_or_argument',1,'p_secrule_operator_or_argument','msc_pyparser.py',936),
  ('secrule_operator_or_argument -> secrule_operator_argument_only','secrule_operator_or_argument',1,'p_secrule_operator_or_argument','msc_pyparser.py',937),
  ('secrule_operator_only -> T_SECRULE_OPERATOR','secrule_operator_only',1,'p_secrule_operator_only','msc_pyparser.py',941),
  ('secrule_operator_only -> T_SECRULE_OPERATOR_WITH_EXCLAMMARK','secrule_operator_only',1,'p_secrule_operator_only','msc_pyparser.py',942),
  ('secrule_operator_argument_only -> T_SECRULE_OPERATOR_ARGUMENT','secrule_operator_argument_only',1,'p_secrule_operator_argument_only','msc_pyparser.py',955),
  ('secrule_operator_and_argument -> T_SECRULE_OPERATOR T_SECRULE_OPERATOR_ARGUMENT','secrule_operator_and_argument',2,'p_secrule_operator_and_argument','msc_pyparser.py',962),
  ('secrule_operator_and_argument -> T_SECRULE_OPERATOR_WITH_EXCLAMMARK T_SECRULE_OPERATOR_ARGUMENT','secrule_operator_and_argument',2,'p_secrule_operator_and_argument','msc_pyparser.py',963),
  ('secrule_actions -> T_SECRULE_ACTION_QUOTE_MARK secrule_actions_list T_SECRULE_ACTION_QUOTE_MARK','secrule_actions',3,'p_secrule_actions','msc_pyparser.py',975),
  ('secrule_actions -> secrule_actions_list','secrule_actions',1,'p_secrule_actions','msc_pyparser.py',976),
  ('secrule_actions_list -> secaction_expr','secrule_actions_list',1,'p_secrule_actions_list','msc_pyparser.py',980),
  ('secrule_actions_list -> secaction_expr_list secaction_expr','secrule_actions_list',2,'p_secrule_actions_list','msc_pyparser.py',981),
  ('secaction_expr_list -> secaction_expr','secaction_expr_list',1,'p_secaction_expr_list','msc_pyparser.py',985),
  ('secaction_expr_list -> secaction_expr_list secaction_expr','secaction_expr_list',2,'p_secaction_expr_list','msc_pyparser.py',986),
  ('secaction_expr -> secaction_single','secaction_expr',1,'p_secaction_expr','msc_pyparser.py',990),
  ('secaction_expr -> secaction_with_argument','secaction_expr',1,'p_secaction_expr','msc_pyparser.py',991),
  ('secaction_expr -> secaction_with_quoted_argument','secaction_expr',1,'p_secaction_expr','msc_pyparser.py',992),
  ('secaction_expr -> secaction_with_argument_with_value','secaction_expr',1,'p_secaction_expr','msc_pyparser.py',993),
  ('secaction_expr -> secaction_with_argument_with_value_and_param','secaction_expr',1,'p_secaction_expr','msc_pyparser.py',994),
  ('secaction_expr -> secaction_with_argument_with_value_and_param_paramarg','secaction_expr',1,'p_secaction_expr','msc_pyparser.py',995),
  ('secaction_expr -> T_SECRULE_ACTION_SEPARATOR','secaction_expr',1,'p_secaction_expr','msc_pyparser.py',996),
  ('secaction_single -> T_SECRULE_ACTION','secaction_single',1,'p_secaction_single','msc_pyparser.py',1000),
  ('secaction_with_argument -> T_SECRULE_ACTION T_SECRULE_ACTION_COLON T_SECRULE_ACTION_ARGUMENT','secaction_with_argument',3,'p_secaction_with_argument','msc_pyparser.py',1004),
  ('secaction_with_quoted_argument -> T_SECRULE_ACTION T_SECRULE_ACTION_COLON T_SECRULE_ACTION_ARGUMENT_QUOTE_SINGLE T_SECRULE_ACTION_ARGUMENT T_SECRULE_ACTION_ARGUMENT_QUOTE_SINGLE','secaction_with_quoted_argument',5,'p_secaction_with_quoted_argument','msc_pyparser.py',1008),
  ('secaction_with_argument_with_value -> T_SECRULE_ACTION T_SECRULE_ACTION_COLON T_SECRULE_ACTION_ARGUMENT T_SECRULE_ACTION_EQUALMARK T_SECRULE_ACTION_ARGUMENT_VALUE','secaction_with_argument_with_value',5,'p_secaction_with_argument_with_value','msc_pyparser.py',1012),
  ('secaction_with_argument_with_value_and_param -> T_SECRULE_ACTION T_SECRULE_ACTION_COLON T_SECRULE_ACTION_ARGUMENT T_SECRULE_ACTION_EQUALMARK T_SECRULE_ACTION_ARGUMENT_VALUE T_SECRULE_ACTION_SEMICOLON T_SECRULE_ACTION_ARGUMENT_VALUE_PARAMETER','secaction_with_argument_with_value_and_param',7,'p_secaction_with_argument_with_value_and_param','msc_pyparser.py',1016),
  ('secaction_with_argument_with_value_and_param_paramarg -> T_SECRULE_ACTION T_SECRULE_ACTION_COLON T_SECRULE_ACTION_ARGUMENT T_SECRULE_ACTION_EQUALMARK T_SECRULE_ACTION_ARGUMENT_VALUE T_SECRULE_ACTION_SEMICOLON T_SECRULE_ACTION_ARGUMENT_VALUE_PARAMETER T_SECRULE_ACTION_ARGUMENT_VALUE_PARAMETER_COLON T_SECRULE_ACTION_ARGUMENT_VALUE_PARAMETER_ARGUMENT','secaction_with_argument_with_value_and_param_paramarg',9,'p_secaction_with_argument_with_value_and_param_paramarg','msc_pyparser.py',1020),
]
