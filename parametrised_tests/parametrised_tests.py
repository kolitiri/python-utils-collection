"""
	Using pytest with custom parametrisation in order to allow
	dynamic test descriptions to be injected in the 'ids' param.

	NOTE: Every function in the test classes should be accompanied
	by a '<function_name>_scenarios' list of parameter dicts.

	Running the script with pytest should produce the following error:

		TestSampleWithScenarios.test_func_1[The description of the second test]

	having successfully injected the description of the test in the 'ids'.
"""
import pytest


def pytest_generate_tests(metafunc):
	""" Custom parametrisation scheme """
	function_name = metafunc.function.__name__
	function_scenarios = getattr(metafunc.cls, f"{function_name}_scenarios")
	function_params = [key for key in function_scenarios[0]]
	function_values = [scenario.values() for scenario in function_scenarios]
	ids_list=[sc.get("description") for sc in function_scenarios]

	metafunc.parametrize(function_params, function_values, ids=ids_list, scope="class")


class TestSampleWithScenarios:

	# Test scenarios for the first test
	test_func_1_scenarios = [
		dict(
			description="The description of the first test",
			param_1=1,
			param_2=1,
		),
		dict(
			description="The description of the second test",
			param_1=2,
			param_2=1,
		),
	]
	@pytest.mark.asyncio
	async def test_func_1(self, description, param_1, param_2):
		assert param_1 == param_2

	# Test scenarios for the second test
	test_func_2_scenarios = [
		dict(
			description="The description of the third test",
			param_1=1,
		),
	]
	@pytest.mark.asyncio
	async def test_func_2(self, description, param_1):
		assert param_1 == 1
